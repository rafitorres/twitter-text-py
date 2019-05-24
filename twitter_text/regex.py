#  encoding=utf-8

# A collection of regular expressions for parsing Tweet text. The regular expression
# list is frozen at load time to ensure immutability. These reular expressions are
# used throughout the Twitter classes. Special care has been taken to make
# sure these reular expressions work with Tweets in all languages.
import re, string

REGEXEN = {} # :nodoc:

def regex_range(start, end = None):
    if end:
        return u'%s-%s' % (unichr(start), unichr(end))
    else:
        return u'%s' % unichr(start)

# Space is more than %20, U+3000 for example is the full-width space used with Kanji. Provide a short-hand
# to access both the list of characters and a pattern suitible for use with String#split
#  Taken from: ActiveSupport::Multibyte::Handlers::UTF8Handler::UNICODE_WHITESPACE
UNICODE_SPACES = []
for space in reduce(lambda x,y: x + y if type(y) == list else x + [y], [
        range(0x0009, 0x000D),  # White_Space # Cc   [5] <control-0009>..<control-000D>
        0x0020,                 # White_Space # Zs       SPACE
        0x0085,                 # White_Space # Cc       <control-0085>
        0x00A0,                 # White_Space # Zs       NO-BREAK SPACE
        0x1680,                 # White_Space # Zs       OGHAM SPACE MARK
        0x180E,                 # White_Space # Zs       MONGOLIAN VOWEL SEPARATOR
        range(0x2000, 0x200A),  # White_Space # Zs  [11] EN QUAD..HAIR SPACE
        0x2028,                 # White_Space # Zl       LINE SEPARATOR
        0x2029,                 # White_Space # Zp       PARAGRAPH SEPARATOR
        0x202F,                 # White_Space # Zs       NARROW NO-BREAK SPACE
        0x205F,                 # White_Space # Zs       MEDIUM MATHEMATICAL SPACE
        0x3000,                 # White_Space # Zs       IDEOGRAPHIC SPACE
    ]):
    UNICODE_SPACES.append(unichr(space))
REGEXEN['spaces'] = re.compile(ur''.join(UNICODE_SPACES))

# Characters not allowed in Tweets
INVALID_CHARACTERS  =   [
    0xFFFE, 0xFEFF,                         # BOM
    0xFFFF,                                 # Special
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E, # Directional change
]
REGEXEN['invalid_control_characters']   =   [unichr(x) for x in INVALID_CHARACTERS]

REGEXEN['list_name'] = re.compile(ur'^[a-zA-Z][a-zA-Z0-9_\-\u0080-\u00ff]{0,24}$')

# Latin accented characters
# Excludes 0xd7 from the range (the multiplication sign, confusable with "x").
# Also excludes 0xf7, the division sign
LATIN_ACCENTS = [
    regex_range(0x00c0, 0x00d6),
    regex_range(0x00d8, 0x00f6),
    regex_range(0x00f8, 0x00ff),
    regex_range(0x0100, 0x024f),
    regex_range(0x0253, 0x0254),
    regex_range(0x0256, 0x0257),
    regex_range(0x0259),
    regex_range(0x025b),
    regex_range(0x0263),
    regex_range(0x0268),
    regex_range(0x026f),
    regex_range(0x0272),
    regex_range(0x0289),
    regex_range(0x028b),
    regex_range(0x02bb),
    regex_range(0x0300, 0x036f),
    regex_range(0x1e00, 0x1eff),
]
REGEXEN['latin_accents'] = re.compile(ur''.join(LATIN_ACCENTS), re.IGNORECASE | re.UNICODE)
LATIN_ACCENTS = u''.join(LATIN_ACCENTS)

RTL_CHARACTERS = ''.join([
    regex_range(0x0600,0x06FF),
    regex_range(0x0750,0x077F),
    regex_range(0x0590,0x05FF),
    regex_range(0xFE70,0xFEFF)
])

NON_LATIN_HASHTAG_CHARS = ''.join([
    # Cyrillic (Russian, Ukrainian, etc.)
    regex_range(0x0400, 0x04ff), # Cyrillic
    regex_range(0x0500, 0x0527), # Cyrillic Supplement
    regex_range(0x2de0, 0x2dff), # Cyrillic Extended A
    regex_range(0xa640, 0xa69f), # Cyrillic Extended B
    regex_range(0x0591, 0x05bf), # Hebrew
    regex_range(0x05c1, 0x05c2),
    regex_range(0x05c4, 0x05c5),
    regex_range(0x05c7),
    regex_range(0x05d0, 0x05ea),
    regex_range(0x05f0, 0x05f4),
    regex_range(0xfb12, 0xfb28), # Hebrew Presentation Forms
    regex_range(0xfb2a, 0xfb36),
    regex_range(0xfb38, 0xfb3c),
    regex_range(0xfb3e),
    regex_range(0xfb40, 0xfb41),
    regex_range(0xfb43, 0xfb44),
    regex_range(0xfb46, 0xfb4f),
    regex_range(0x0610, 0x061a), # Arabic
    regex_range(0x0620, 0x065f),
    regex_range(0x066e, 0x06d3),
    regex_range(0x06d5, 0x06dc),
    regex_range(0x06de, 0x06e8),
    regex_range(0x06ea, 0x06ef),
    regex_range(0x06fa, 0x06fc),
    regex_range(0x06ff),
    regex_range(0x0750, 0x077f), # Arabic Supplement
    regex_range(0x08a0),         # Arabic Extended A
    regex_range(0x08a2, 0x08ac),
    regex_range(0x08e4, 0x08fe),
    regex_range(0xfb50, 0xfbb1), # Arabic Pres. Forms A
    regex_range(0xfbd3, 0xfd3d),
    regex_range(0xfd50, 0xfd8f),
    regex_range(0xfd92, 0xfdc7),
    regex_range(0xfdf0, 0xfdfb),
    regex_range(0xfe70, 0xfe74), # Arabic Pres. Forms B
    regex_range(0xfe76, 0xfefc),
    regex_range(0x200c, 0x200c), # Zero-Width Non-Joiner
    regex_range(0x0e01, 0x0e3a), # Thai
    regex_range(0x0e40, 0x0e4e), # Hangul (Korean)
    regex_range(0x1100, 0x11ff), # Hangul Jamo
    regex_range(0x3130, 0x3185), # Hangul Compatibility Jamo
    regex_range(0xA960, 0xA97F), # Hangul Jamo Extended-A
    regex_range(0xAC00, 0xD7AF), # Hangul Syllables
    regex_range(0xD7B0, 0xD7FF), # Hangul Jamo Extended-B
    regex_range(0xFFA1, 0xFFDC)  # Half-width Hangul
])

CJ_HASHTAG_CHARACTERS = ''.join([
    regex_range(0x30A1, 0x30FA), regex_range(0x30FC, 0x30FE), # Katakana (full-width)
    regex_range(0xFF66, 0xFF9F), # Katakana (half-width)
    regex_range(0xFF10, 0xFF19), regex_range(0xFF21, 0xFF3A), regex_range(0xFF41, 0xFF5A), # Latin (full-width)
    regex_range(0x3041, 0x3096), regex_range(0x3099, 0x309E), # Hiragana
    regex_range(0x3400, 0x4DBF), # Kanji (CJK Extension A)
    regex_range(0x4E00, 0x9FFF), # Kanji (Unified)
])

try:
    CJ_HASHTAG_CHARACTERS = ''.join([
        CJ_HASHTAG_CHARACTERS,
        regex_range(0x20000, 0x2A6DF), # Kanji (CJK Extension B)
        regex_range(0x2A700, 0x2B73F), # Kanji (CJK Extension C)
        regex_range(0x2B740, 0x2B81F), # Kanji (CJK Extension D)
        regex_range(0x2F800, 0x2FA1F), regex_range(0x3003), regex_range(0x3005), regex_range(0x303B) # Kanji (CJK supplement)
    ])
except ValueError:
    # this is a narrow python build so these extended Kanji characters won't work
    pass

PUNCTUATION_CHARS = ur'!"#$%&\'()*+,-./:;<=>?@\[\]^_\`{|}~'
SPACE_CHARS = ur" \t\n\x0B\f\r"
CTRL_CHARS = ur"\x00-\x1F\x7F"

# A hashtag must contain latin characters, numbers and underscores, but not all numbers.
HASHTAG_ALPHA = ur'[a-z_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)
HASHTAG_ALPHANUMERIC = ur'[a-z0-9_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)
HASHTAG_BOUNDARY = ur'\A|\z|\[|[^&a-z0-9_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)

HASHTAG = re.compile(ur'(%s)(#|＃)(%s*%s%s*)' % (HASHTAG_BOUNDARY, HASHTAG_ALPHANUMERIC, HASHTAG_ALPHA, HASHTAG_ALPHANUMERIC), re.IGNORECASE)

REGEXEN['valid_hashtag'] = HASHTAG
REGEXEN['end_hashtag_match'] = re.compile(ur'\A(?:[#＃]|:\/\/)', re.IGNORECASE | re.UNICODE)
REGEXEN['numeric_only'] = re.compile(ur'^[\d]+$')

REGEXEN['valid_mention_preceding_chars'] = re.compile(r'(?:[^a-zA-Z0-9_!#\$%&*@＠]|^|RT:?)')
REGEXEN['at_signs'] = re.compile(ur'[@＠]')
REGEXEN['valid_mention_or_list'] = re.compile(
    ur'(%s)' % REGEXEN['valid_mention_preceding_chars'].pattern.decode('utf-8') +   # preceding character
    ur'(%s)' % REGEXEN['at_signs'].pattern +                                        # at mark
    ur'([a-zA-Z0-9_]{1,20})' +                                                      # screen name
    ur'(\/[a-zA-Z][a-zA-Z0-9_\-]{0,24})?'                                           # list (optional)
)
REGEXEN['valid_reply'] = re.compile(ur'^(?:[%s])*%s([a-zA-Z0-9_]{1,20})' % (REGEXEN['spaces'].pattern, REGEXEN['at_signs'].pattern), re.IGNORECASE | re.UNICODE)
 # Used in Extractor for final filtering
REGEXEN['end_mention_match'] = re.compile(ur'\A(?:%s|[%s]|:\/\/)' % (REGEXEN['at_signs'].pattern, REGEXEN['latin_accents'].pattern), re.IGNORECASE | re.UNICODE)

# URL related hash regex collection
REGEXEN['valid_url_preceding_chars'] = re.compile(ur'(?:[^A-Z0-9@＠$#＃%s]|^)' % ur''.join(REGEXEN['invalid_control_characters']), re.IGNORECASE | re.UNICODE)
REGEXEN['invalid_url_without_protocol_preceding_chars'] = re.compile(ur'[-_.\/]$')
DOMAIN_VALID_CHARS = ur'[^%s%s%s%s%s]' % (PUNCTUATION_CHARS, SPACE_CHARS, CTRL_CHARS, ur''.join(REGEXEN['invalid_control_characters']), ur''.join(UNICODE_SPACES))
REGEXEN['valid_subdomain'] = re.compile(ur'(?:(?:%s(?:[_-]|%s)*)?%s\.)' % (DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS), re.IGNORECASE | re.UNICODE)
REGEXEN['valid_domain_name'] = re.compile(ur'(?:(?:%s(?:[-]|%s)*)?%s\.)' % (DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS), re.IGNORECASE | re.UNICODE)
REGEXEN['valid_gTLD'] = re.compile(ur'(?:(?:aarp|abarth|abb|abbott|abbvie|abc|able|abogado|abudhabi|academy|accenture|accountant|accountants|aco|active|actor|adac|ads|adult|aeg|aetna|afamilycompany|afl|africa|agakhan|agency|aig|aigo|airbus|airforce|airtel|akdn|alfaromeo|alibaba|alipay|allfinanz|allstate|ally|alsace|alstom|americanexpress|americanfamily|amex|amfam|amica|amsterdam|analytics|android|anquan|anz|aol|apartments|app|apple|aquarelle|arab|aramco|archi|army|art|arte|asda|associates|athleta|attorney|auction|audi|audible|audio|auspost|author|auto|autos|avianca|aws|axa|azure|baby|baidu|banamex|bananarepublic|band|bank|bar|barcelona|barclaycard|barclays|barefoot|bargains|baseball|basketball|bauhaus|bayern|bbc|bbt|bbva|bcg|bcn|beats|beauty|beer|bentley|berlin|best|bestbuy|bet|bharti|bible|bid|bike|bing|bingo|bio|black|blackfriday|blanco|blockbuster|blog|bloomberg|blue|bms|bmw|bnl|bnpparibas|boats|boehringer|bofa|bom|bond|boo|book|booking|boots|bosch|bostik|boston|bot|boutique|box|bradesco|bridgestone|broadway|broker|brother|brussels|budapest|bugatti|build|builders|business|buy|buzz|bzh|cab|cafe|cal|call|calvinklein|cam|camera|camp|cancerresearch|canon|capetown|capital|capitalone|car|caravan|cards|care|career|careers|cars|cartier|casa|case|caseih|cash|casino|catering|catholic|cba|cbn|cbre|cbs|ceb|center|ceo|cern|cfa|cfd|chanel|channel|charity|chase|chat|cheap|chintai|chloe|christmas|chrome|chrysler|church|cipriani|circle|cisco|citadel|citi|citic|city|cityeats|claims|cleaning|click|clinic|clinique|clothing|cloud|club|clubmed|coach|codes|coffee|college|cologne|com|comcast|commbank|community|company|compare|computer|comsec|condos|construction|consulting|contact|contractors|cooking|cookingchannel|cool|corsica|country|coupon|coupons|courses|credit|creditcard|creditunion|cricket|crown|crs|cruise|cruises|csc|cuisinella|cymru|cyou|dabur|dad|dance|data|date|dating|datsun|day|dclk|dds|deal|dealer|deals|degree|delivery|dell|deloitte|delta|democrat|dental|dentist|desi|design|dev|dhl|diamonds|diet|digital|direct|directory|discount|discover|dish|diy|dnp|docs|doctor|dodge|dog|doha|domains|doosan|dot|download|drive|dtv|dubai|duck|dunlop|duns|dupont|durban|dvag|dvr|earth|eat|eco|edeka|education|email|emerck|energy|engineer|engineering|enterprises|epost|epson|equipment|ericsson|erni|esq|estate|esurance|etisalat|eurovision|eus|events|everbank|exchange|expert|exposed|express|extraspace|fage|fail|fairwinds|faith|family|fan|fans|farm|farmers|fashion|fast|fedex|feedback|ferrari|ferrero|fiat|fidelity|fido|film|final|finance|financial|fire|firestone|firmdale|fish|fishing|fit|fitness|flickr|flights|flir|florist|flowers|flsmidth|fly|foo|food|foodnetwork|football|ford|forex|forsale|forum|foundation|fox|free|fresenius|frl|frogans|frontdoor|frontier|ftr|fujitsu|fujixerox|fun|fund|furniture|futbol|fyi|gal|gallery|gallo|gallup|game|games|gap|garden|gbiz|gdn|gea|gent|genting|george|ggee|gift|gifts|gives|giving|glade|glass|gle|global|globo|gmail|gmbh|gmo|gmx|godaddy|gold|goldpoint|golf|goo|goodhands|goodyear|goog|google|gop|got|grainger|graphics|gratis|green|gripe|grocery|group|guardian|gucci|guge|guide|guitars|guru|hair|hamburg|hangout|haus|hbo|hdfc|hdfcbank|health|healthcare|help|helsinki|here|hermes|hgtv|hiphop|hisamitsu|hitachi|hiv|hkt|hockey|holdings|holiday|homedepot|homegoods|homes|homesense|honda|honeywell|horse|hospital|host|hosting|hot|hoteles|hotels|hotmail|house|how|hsbc|htc|hughes|hyatt|hyundai|ibm|icbc|ice|icu|ieee|ifm|iinet|ikano|imamat|imdb|immo|immobilien|industries|infiniti|info|ing|ink|institute|insurance|insure|intel|international|intuit|investments|ipiranga|irish|iselect|ismaili|ist|istanbul|itau|itv|iveco|iwc|jaguar|java|jcb|jcp|jeep|jetzt|jewelry|jio|jlc|jll|jmp|jnj|joburg|jot|joy|jpmorgan|jprs|juegos|juniper|kaufen|kddi|kerryhotels|kerrylogistics|kerryproperties|kfh|kia|kim|kinder|kindle|kitchen|kiwi|koeln|komatsu|kosher|kpmg|kpn|krd|kred|kuokgroup|kyoto|lacaixa|ladbrokes|lamborghini|lamer|lancaster|lancia|lancome|land|landrover|lanxess|lasalle|lat|latino|latrobe|law|lawyer|lds|lease|leclerc|lefrak|legal|lego|lexus|lgbt|liaison|lidl|life|lifeinsurance|lifestyle|lighting|like|lilly|limited|limo|lincoln|linde|link|lipsy|live|living|lixil|llc|loan|loans|locker|locus|loft|lol|london|lotte|lotto|love|lpl|lplfinancial|ltd|ltda|lundbeck|lupin|luxe|luxury|macys|madrid|maif|maison|makeup|man|management|mango|map|market|marketing|markets|marriott|marshalls|maserati|mattel|mba|mcd|mcdonalds|mckinsey|med|media|meet|melbourne|meme|memorial|men|menu|meo|merckmsd|metlife|miami|microsoft|mini|mint|mit|mitsubishi|mlb|mls|mma|mobi|mobile|mobily|moda|moe|moi|mom|monash|money|monster|montblanc|mopar|mormon|mortgage|moscow|moto|motorcycles|mov|movie|movistar|msd|mtn|mtpc|mtr|mutual|mutuelle|nab|nadex|nagoya|nationwide|natura|navy|nba|nec|net|netbank|netflix|network|neustar|new|newholland|news|next|nextdirect|nexus|nfl|ngo|nhk|nico|nike|nikon|ninja|nissan|nissay|nokia|northwesternmutual|norton|now|nowruz|nowtv|nra|nrw|ntt|nyc|obi|observer|off|office|okinawa|olayan|olayangroup|oldnavy|ollo|omega|one|ong|onl|online|onyourside|ooo|open|oracle|orange|org|organic|orientexpress|origins|osaka|otsuka|ott|ovh|page|pamperedchef|panasonic|panerai|paris|pars|partners|parts|party|passagens|pay|pccw|pet|pfizer|pharmacy|phd|philips|phone|photo|photography|photos|physio|piaget|pics|pictet|pictures|pid|pin|ping|pink|pioneer|pizza|place|play|playstation|plumbing|plus|pnc|pohl|poker|politie|porn|pramerica|praxi|press|prime|prod|productions|prof|progressive|promo|properties|property|protection|pru|prudential|pub|pwc|qpon|quebec|quest|qvc|racing|radio|raid|read|realestate|realtor|realty|recipes|red|redstone|redumbrella|rehab|reise|reisen|reit|reliance|ren|rent|rentals|repair|report|republican|rest|restaurant|review|reviews|rexroth|rich|richardli|ricoh|rightathome|ril|rio|rip|rmit|rocher|rocks|rodeo|rogers|room|rsvp|rugby|ruhr|run|rwe|ryukyu|saarland|safe|safety|sakura|sale|salon|samsclub|samsung|sandvik|sandvikcoromant|sanofi|sap|sapo|sarl|sas|save|saxo|sbi|sbs|sca|scb|schaeffler|schmidt|scholarships|school|schule|schwarz|science|scjohnson|scor|scot|search|seat|secure|security|seek|select|sener|services|ses|seven|sew|sex|sexy|sfr|shangrila|sharp|shaw|shell|shia|shiksha|shoes|shop|shopping|shouji|show|showtime|shriram|silk|sina|singles|site|ski|skin|sky|skype|sling|smart|smile|sncf|soccer|social|softbank|software|sohu|solar|solutions|song|sony|soy|space|spiegel|sport|spot|spreadbetting|srl|srt|stada|staples|star|starhub|statebank|statefarm|statoil|stc|stcgroup|stockholm|storage|store|stream|studio|study|style|sucks|supplies|supply|support|surf|surgery|suzuki|swatch|swiftcover|swiss|sydney|symantec|systems|tab|taipei|talk|taobao|target|tatamotors|tatar|tattoo|tax|taxi|tci|tdk|team|tech|technology|telecity|telefonica|temasek|tennis|teva|thd|theater|theatre|tiaa|tickets|tienda|tiffany|tips|tires|tirol|tjmaxx|tjx|tkmaxx|tmall|today|tokyo|tools|top|toray|toshiba|total|tours|town|toyota|toys|trade|trading|training|travelchannel|travelers|travelersinsurance|trust|trv|tube|tui|tunes|tushu|tvs|ubank|ubs|uconnect|unicom|university|uno|uol|ups|vacations|vana|vanguard|vegas|ventures|verisign|versicherung|vet|viajes|video|vig|viking|villas|vin|vip|virgin|visa|vision|vista|vistaprint|viva|vivo|vlaanderen|vodka|volkswagen|volvo|vote|voting|voto|voyage|vuelos|wales|walmart|walter|wang|wanggou|warman|watch|watches|weather|weatherchannel|webcam|weber|website|wed|wedding|weibo|weir|whoswho|wien|wiki|williamhill|win|windows|wine|winners|wme|wolterskluwer|woodside|work|works|world|wow|wtc|wtf|xbox|xerox|xfinity|xihuan|xin|कॉम|セール|佛山|慈善|集团|在线|大众汽车|点看|คอม|八卦|‏موقع‎|公益|公司|香格里拉|网站|移动|我爱你|москва|католик|онлайн|сайт|联通|‏קום‎|时尚|微博|淡马锡|ファッション|орг|नेट|ストア|삼성|商标|商店|商城|дети|ポイント|新闻|工行|家電|‏كوم‎|中文网|中信|娱乐|谷歌|電訊盈科|购物|クラウド|通販|网店|संगठन|餐厅|网络|ком|诺基亚|食品|飞利浦|手表|手机|‏ارامكو‎|‏العليان‎|‏اتصالات‎|‏بازار‎|‏موبايلي‎|‏ابوظبي‎|‏كاثوليك‎|‏همراه‎|닷컴|政府|‏شبكة‎|‏بيتك‎|‏عرب‎|机构|组织机构|健康|招聘|рус|珠宝|大拿|みんな|グーグル|世界|書籍|网址|닷넷|コム|天主教|游戏|vermögensberater|vermögensberatung|企业|信息|嘉里大酒店|嘉里|广东|政务|xperia|xyz|yachts|yahoo|yamaxun|yandex|yodobashi|yoga|yokohama|you|youtube|yun|zappos|zara|zero|zip|zippo|zone|zuerich|biz|name|pro|arpa|aero|asia|cat|coop|edu|gov|int|jobs|mil|museum|post|tel|travel|xxx)(?=[^0-9a-z]|$))', re.IGNORECASE | re.UNICODE)
REGEXEN['valid_ccTLD'] = re.compile(ur'(?:(?:ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bl|bm|bn|bo|bq|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cw|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mf|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ಭಾರತ|한국|ଭାରତ|ভাৰত|ভারত|বাংলা|қаз|срб|бг|бел|சிங்கப்பூர்|мкд|ею|中国|中國|భారత్|ලංකා|ભારત|भारतम्|भारत|भारोत|укр|香港|台湾|台灣|мон|‏الجزائر‎|‏عمان‎|‏ایران‎|‏امارات‎|‏موريتانيا‎|‏پاکستان‎|‏الاردن‎|‏بارت‎|‏بھارت‎|‏المغرب‎|‏السعودية‎|‏ڀارت‎|‏سودان‎|‏عراق‎|‏مليسيا‎|澳門|გე|ไทย|‏سورية‎|рф|‏تونس‎|ελ|ഭാരതം|ਭਾਰਤ|‏مصر‎|‏قطر‎|இலங்கை|இந்தியா|հայ|新加坡|‏فلسطين‎|ye|yt|za|zm|zw)(?=[^0-9a-z]|$))', re.IGNORECASE | re.UNICODE)
REGEXEN['valid_punycode'] = re.compile(ur'(?:xn--[0-9a-z]+)', re.IGNORECASE | re.UNICODE)

REGEXEN['valid_domain'] = re.compile(ur'(?:%s*%s(?:%s|%s|%s))' % (REGEXEN['valid_subdomain'].pattern, REGEXEN['valid_domain_name'].pattern, REGEXEN['valid_gTLD'].pattern, REGEXEN['valid_ccTLD'].pattern, REGEXEN['valid_punycode'].pattern), re.IGNORECASE | re.UNICODE)

# This is used in Extractor
REGEXEN['valid_ascii_domain'] = re.compile(ur'(?:(?:[A-Za-z0-9\-_]|[%s])+\.)+(?:%s|%s|%s)' % (REGEXEN['latin_accents'].pattern, REGEXEN['valid_gTLD'].pattern, REGEXEN['valid_ccTLD'].pattern, REGEXEN['valid_punycode'].pattern), re.IGNORECASE | re.UNICODE)

# This is used in Extractor for stricter t.co URL extraction
REGEXEN['valid_tco_url'] = re.compile(ur'^https?:\/\/t\.co\/[a-z0-9]+', re.IGNORECASE | re.UNICODE)

# This is used in Extractor to filter out unwanted URLs.
REGEXEN['invalid_short_domain'] = re.compile(ur'\A%s%s\Z' % (REGEXEN['valid_domain_name'].pattern, REGEXEN['valid_ccTLD'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['valid_port_number'] = re.compile(ur'[0-9]+')

REGEXEN['valid_general_url_path_chars'] = re.compile(ur"[a-z0-9!\*';:=\+\,\.\$\/%%#\[\]\-_~&|@%s]" % LATIN_ACCENTS, re.IGNORECASE | re.UNICODE)
# Allow URL paths to contain balanced parens
#  1. Used in Wikipedia URLs like /Primer_(film)
#  2. Used in IIS sessions like /S(dfd346)/
REGEXEN['valid_url_balanced_parens'] = re.compile(ur'\(%s+\)' % REGEXEN['valid_general_url_path_chars'].pattern, re.IGNORECASE | re.UNICODE)
# Valid end-of-path chracters (so /foo. does not gobble the period).
#   1. Allow =&# for empty URL parameters and other URL-join artifacts
REGEXEN['valid_url_path_ending_chars'] = re.compile(ur'[a-z0-9=_#\/\+\-%s]|(?:%s)' % (LATIN_ACCENTS, REGEXEN['valid_url_balanced_parens'].pattern), re.IGNORECASE | re.UNICODE)
REGEXEN['valid_url_path'] = re.compile(ur'(?:(?:%s*(?:%s %s*)*%s)|(?:%s+\/))' % (REGEXEN['valid_general_url_path_chars'].pattern, REGEXEN['valid_url_balanced_parens'].pattern, REGEXEN['valid_general_url_path_chars'].pattern, REGEXEN['valid_url_path_ending_chars'].pattern, REGEXEN['valid_general_url_path_chars'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['valid_url_query_chars'] = re.compile(ur"[a-z0-9!?\*'\(\);:&=\+\$\/%#\[\]\-_\.,~|@]", re.IGNORECASE | re.UNICODE)
REGEXEN['valid_url_query_ending_chars'] = re.compile(ur'[a-z0-9_&=#\/]', re.IGNORECASE | re.UNICODE)
REGEXEN['valid_url'] = re.compile(ur'((%s)((https?:\/\/)?(%s)(?::(%s))?(/%s*)?(\?%s*%s)?))' % (
    REGEXEN['valid_url_preceding_chars'].pattern,
    REGEXEN['valid_domain'].pattern,
    REGEXEN['valid_port_number'].pattern,
    REGEXEN['valid_url_path'].pattern,
    REGEXEN['valid_url_query_chars'].pattern,
    REGEXEN['valid_url_query_ending_chars'].pattern
), re.IGNORECASE | re.UNICODE)
#   Matches
#   $1 total match
#   $2 Preceeding chracter
#   $3 URL
#   $4 Protocol (optional)
#   $5 Domain(s)
#   $6 Port number (optional)
#   $7 URL Path and anchor
#   $8 Query String

REGEXEN['cashtag'] = re.compile(ur'[a-z]{1,6}(?:[._][a-z]{1,2})?', re.IGNORECASE)
REGEXEN['valid_cashtag'] = re.compile(ur'(^|[%s])(\$|＄|﹩)(%s)(?=$|\s|[%s])' % (REGEXEN['spaces'].pattern, REGEXEN['cashtag'].pattern, PUNCTUATION_CHARS), re.IGNORECASE)

# These URL validation pattern strings are based on the ABNF from RFC 3986
REGEXEN['validate_url_unreserved'] = re.compile(ur'[a-z0-9\-._~]', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_pct_encoded'] = re.compile(ur'(?:%[0-9a-f]{2})', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_sub_delims'] = re.compile(ur"[!$&'()*+,;=]", re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_pchar'] = re.compile(ur'(?:%s|%s|%s|[:\|@])' % (REGEXEN['validate_url_unreserved'].pattern, REGEXEN['validate_url_pct_encoded'].pattern, REGEXEN['validate_url_sub_delims'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_scheme'] = re.compile(ur'(?:[a-z][a-z0-9+\-.]*)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_userinfo'] = re.compile(ur'(?:%s|%s|%s|:)*' % (REGEXEN['validate_url_unreserved'].pattern, REGEXEN['validate_url_pct_encoded'].pattern, REGEXEN['validate_url_sub_delims'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_dec_octet'] = re.compile(ur'(?:[0-9]|(?:[1-9][0-9])|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5]))', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_ipv4'] = re.compile(ur'(?:%s(?:\.%s){3})' % (REGEXEN['validate_url_dec_octet'].pattern, REGEXEN['validate_url_dec_octet'].pattern), re.IGNORECASE | re.UNICODE)

# Punting on real IPv6 validation for now
REGEXEN['validate_url_ipv6'] = re.compile(ur'(?:\[[a-f0-9:\.]+\])', re.IGNORECASE | re.UNICODE)

# Also punting on IPvFuture for now
REGEXEN['validate_url_ip'] = re.compile(ur'(?:%s|%s)' % (REGEXEN['validate_url_ipv4'].pattern, REGEXEN['validate_url_ipv6'].pattern), re.IGNORECASE | re.UNICODE)

# This is more strict than the rfc specifies
REGEXEN['validate_url_subdomain_segment'] = re.compile(ur'(?:[a-z0-9](?:[a-z0-9_\-]*[a-z0-9])?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_domain_segment'] = re.compile(ur'(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_domain_tld'] = re.compile(ur'(?:[a-z](?:[a-z0-9\-]*[a-z0-9])?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_domain'] = re.compile(ur'(?:(?:%s\.)*(?:%s\.)%s)' % (REGEXEN['validate_url_subdomain_segment'].pattern, REGEXEN['validate_url_domain_segment'].pattern, REGEXEN['validate_url_domain_tld'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_host'] = re.compile(ur'(?:%s|%s)' % (REGEXEN['validate_url_ip'].pattern, REGEXEN['validate_url_domain'].pattern), re.IGNORECASE | re.UNICODE)

# Unencoded internationalized domains - this doesn't check for invalid UTF-8 sequences
REGEXEN['validate_url_unicode_subdomain_segment'] = re.compile(ur'(?:(?:[a-z0-9]|[^\x00-\x7f])(?:(?:[a-z0-9_\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_unicode_domain_segment'] = re.compile(ur'(?:(?:[a-z0-9]|[^\x00-\x7f])(?:(?:[a-z0-9\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_unicode_domain_tld'] = re.compile(ur'(?:(?:[a-z]|[^\x00-\x7f])(?:(?:[a-z0-9\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_unicode_domain'] = re.compile(ur'(?:(?:%s\.)*(?:%s\.)%s)' % (REGEXEN['validate_url_unicode_subdomain_segment'].pattern, REGEXEN['validate_url_unicode_domain_segment'].pattern, REGEXEN['validate_url_unicode_domain_tld'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_unicode_host'] = re.compile(ur'(?:%s|%s)' % (REGEXEN['validate_url_ip'].pattern, REGEXEN['validate_url_unicode_domain'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_port'] = re.compile(ur'[0-9]{1,5}')

REGEXEN['validate_url_unicode_authority'] = re.compile(ur'(?:(%s)@)?(%s)(?::(%s))?' % (REGEXEN['validate_url_userinfo'].pattern, REGEXEN['validate_url_unicode_host'].pattern, REGEXEN['validate_url_port'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_authority'] = re.compile(ur'(?:(%s)@)?(%s)(?::(%s))?' % (REGEXEN['validate_url_userinfo'].pattern, REGEXEN['validate_url_host'].pattern, REGEXEN['validate_url_port'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_path'] = re.compile(ur'(/%s*)*' % REGEXEN['validate_url_pchar'].pattern, re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_query'] = re.compile(ur'(%s|/|\?)*' % REGEXEN['validate_url_pchar'].pattern, re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_fragment'] = re.compile(ur'(%s|/|\?)*' % REGEXEN['validate_url_pchar'].pattern, re.IGNORECASE | re.UNICODE)

# Modified version of RFC 3986 Appendix B
REGEXEN['validate_url_unencoded'] = re.compile(ur'\A(?:([^:/?#]+)://)?([^/?#]*)([^?#]*)(?:\?([^#]*))?(?:\#(.*))?\Z', re.IGNORECASE | re.UNICODE)

REGEXEN['rtl_chars'] = re.compile(ur'[%s]' % RTL_CHARACTERS, re.IGNORECASE | re.UNICODE)
