import re
import unicodedata

import pandas as pd


UNKNOWN_VALUES = {"", "nan", "none", "null", "other"}


def _clean_value(value):
    if pd.isna(value):
        return None, "null"

    original = unicodedata.normalize("NFKC", str(value).strip())
    original = original.translate(str.maketrans({"Х": "X", "х": "x", "М": "M", "м": "m"}))
    s = original.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()

    if s in UNKNOWN_VALUES:
        return None, original.lower()

    return s, original.lower()


def _unknown(original):
    return "unknown"


def _match_patterns(s, patterns):
    for canonical, pattern in patterns:
        if re.search(pattern, s):
            return canonical
    return None


def _normalize_ford_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    s = s.replace("fusiom", "fusion")
    s = s.replace("fussion", "fusion")
    s = s.replace("turus", "taurus")
    s = s.replace("rnger", "ranger")
    s = s.replace("expidition", "expedition")
    s = s.replace("explore ", "explorer ")

    if "sterling l7500" in s:
        return "sterling l7500"

    priority_patterns = [
        ("mustang", r"mustang|shelby"),
        ("explorer", r"explorer.*police interceptor|police interceptor.*explorer"),
        ("taurus", r"taurus.*police interceptor|police interceptor.*taurus"),
        ("focus", r"focus"),
        ("e-450", r"^e\s*450\b|^e450\b"),
        ("e-350", r"^e\s*350\b|^e350\b"),
        ("e-250", r"^e\s*250\b|^e250\b"),
        ("e-series / econoline", r"^e\s*150\b|^e150\b"),
    ]
    match = _match_patterns(s, priority_patterns)
    if match:
        return match

    if "econoline" in s or "ecoline" in s or "econline" in s or "ecnoline" in s or "e series" in s:
        if re.search(r"\be\s*-?\s*450\b|\be450\b", s):
            return "e-450"
        if re.search(r"\be\s*-?\s*350\b|\be350\b", s):
            return "e-350"
        if re.search(r"\be\s*-?\s*250\b|\be250\b", s):
            return "e-250"
        if re.search(r"\be\s*-?\s*150\b|\be150\b", s):
            return "e-series / econoline"
        return "e-series / econoline"

    patterns = [
        ("transit connect", r"transit connect|connect xlt"),
        ("transit 150", r"transit\s*t?\s*150|transit cargo 150|\bt\s*-?\s*150\b|t150"),
        ("transit 250", r"transit\s*t?\s*250|transit 250|transit-250|\bt\s*-?\s*250\b|t250"),
        ("transit 350", r"transit\s*350|transit-350|\bt\s*-?\s*350\b|t350"),
        ("transit", r"transit|tranist|trasit|tansit"),
        ("e-450", r"\be\s*450\b|\be450\b"),
        ("e-350", r"\be\s*350\b|\be350\b|e\s*van|3500 triton|truck xl van"),
        ("e-250", r"\be\s*250\b|\be250\b"),
        ("e-150", r"\be\s*150\b|\be150\b|club wagon"),
        ("f-59 stripped chassis", r"\bf\s*59\b|\bf59\b"),
        ("f-800", r"\bf\s*800\b|\bf800\b"),
        ("f-750", r"\bf\s*750\b|\bf750\b|\b750\b"),
        ("f-650", r"\bf\s*650\b|\bf650\b"),
        ("f-550 super duty", r"\bf\s*550\b|\bf550\b|\b550sd\b|\b550\b"),
        ("f-450 super duty", r"\bf\s*450\b|\bf450\b|\b450\b|450\s*750"),
        ("f-350 super duty", r"\bf\s*350\b|\bf350\b|super duty f 350|\b350\b|\bf35o\b|\bf\s*330\b|\bf330\b|\bf\s*360\b|\bf360\b"),
        ("f-250 super duty", r"\bf\s*250\b|\bf250\b|ford250|super duty f 250|\b250\b|\bf25\b"),
        ("f-150", r"\bf\s*150\b|\bf150\b|\b150\b|\bf l50\b|\bf150xl\b"),
        ("e-150", r"\be\s*150\b|\be150\b|club wagon"),
        ("e-250", r"\be\s*250\b|\be250\b"),
        ("e-350", r"\be\s*350\b|\be350\b|e\s*van|3500 triton|truck xl van"),
        ("e-450", r"\be\s*450\b|\be450\b"),
    ]
    match = _match_patterns(s, patterns)
    if match:
        return match

    patterns = [
        ("transit connect", r"transit connect|connect xlt"),
        ("transit 150", r"transit\s*t?\s*150|transit cargo 150"),
        ("transit 250", r"transit\s*t?\s*250|transit 250|transit-250|\bt\s*250\b|t250"),
        ("transit 350", r"transit\s*350|transit-350|\bt\s*350\b|t350"),
        ("transit", r"transit|tranist|trasit|tansit"),
        ("explorer sport trac", r"sports? trac"),
        ("expedition max", r"expedition max"),
        ("expedition el", r"expedition el|expadition el|expetion el"),
        ("fusion energi", r"fusion energi"),
        ("fusion hybrid", r"fusion hybrid|fusion se hybrid"),
        ("c-max energi", r"c max energi|cmax energi"),
        ("c-max hybrid", r"c max|cmax"),
        ("taurus x", r"taurus x|taurux"),
        ("taurus", r"\bsho\b"),
        ("crown victoria", r"crown vic|crown victoria|criwn victoria|crow victoria|police interceptor p7[1b]"),
        ("f-super duty", r"f super duty|f superduty|f super dudy|f superduty|superduty|super duty"),
        ("five hundred", r"\b500\b"),
        ("f-700", r"\bf\s*700\b|\bf700\b"),
        ("f-450 super duty", r"\bf\s*45\b|\bf45\b"),
        ("f-250 super duty", r"\bf\s*25\b|\bf25\b|\bf-25\b"),
        ("f-series", r"\bf series\b|\bf-series\b"),
    ]
    match = _match_patterns(s, patterns)
    if match:
        return match

    contains = [
        "ranger",
        "bronco",
        "ecosport",
        "escape",
        "edge",
        "explorer",
        "expedition",
        "excursion",
        "flex",
        "mustang",
        "thunderbird",
        "focus",
        "escort",
        "contour",
        "fiesta",
        "fusion",
        "taurus",
        "five hundred",
        "freestyle",
        "freestar",
        "windstar",
    ]
    for model in contains:
        if model in s:
            return model
    replacements = {
        "aerostar": "aerostar",
        "aspire": "aspire",
        "beonco": "bronco",
        "eacape": "escape",
        "ecape": "escape",
        "ecoline": "e-series / econoline",
        "eonoline": "e-series / econoline",
        "echosport": "ecosport",
        "egde": "edge",
        "esdge": "edge",
        "esape": "escape",
        "escapre": "escape",
        "excape": "escape",
        "excusrion": "excursion",
        "exolorer": "explorer",
        "exploror": "explorer",
        "exployer": "explorer",
        "explrer": "explorer",
        "expedetion": "expedition",
        "expediton": "expedition",
        "expedtion": "expedition",
        "fuison": "fusion",
        "fustion": "fusion",
        "lighting": "f-150",
        "lightning": "f-150",
        "probe": "probe",
        "tarus": "taurus",
        "tuarus": "taurus",
        "winstar": "windstar",
        "tbird": "thunderbird",
        "t bird": "thunderbird",
        "clubwagon": "e-150",
        "festiva": "festiva",
        "shelby": "mustang",
        "sort trac": "explorer sport trac",
        "sporttrac": "explorer sport trac",
        "sporttrax": "explorer sport trac",
        "tarsus": "taurus",
        "fleeside": "f-150",
        "fles": "f-150",
        "fx4": "f-150",
        "lariat supercrew": "f-150",
        "powerstroke diesel": "f-250 super duty",
        "stepvan": "e-series / econoline",
        "step van": "e-series / econoline",
    }
    for alias, model in replacements.items():
        if alias in s:
            return model
    if s.startswith("gt premium") or "police interceptor" in s:
        return "mustang" if s.startswith("gt premium") else "taurus"

    return _unknown(original)


def _normalize_chevrolet_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    s = s.replace("chevy", "chevrolet")
    patterns = [
        ("express 3500", r"express.*3500|3500.*express|3500.*van|g3500"),
        ("express 2500", r"express.*2500|2500.*express|2500.*van|g2500"),
        ("express 1500", r"express.*1500|1500.*express"),
        ("astro", r"astro"),
        ("uplander", r"uplander|up lander"),
        ("trailblazer", r"trailblazer|trail blazer|trailbalzer|trailblazee|trailblazser"),
        ("blazer", r"blazer"),
        ("avalanche", r"avalanche|avalance|avalache|alalanche|black diamond"),
        ("colorado", r"colorado|colorad"),
        ("tahoe", r"tahoe|taho"),
        ("suburban", r"suburban|susburban"),
        ("malibu", r"malibu|malibi|maibu"),
        ("camaro", r"camaro|comaro|camro|z28"),
        ("monte carlo", r"monte carlo|\bmonte\b"),
        ("trailblazer", r"trailblazer|trail blazer|trailbalzer|trailblazee|trailblazser"),
        ("traverse", r"traverse|travers|treverse|travese|traversa|raverse"),
        ("hhr", r"\bhhr\b"),
        ("silverado 3500 hd", r"silverado.*3500|silverad.*3500|3500.*silverado|3500hd|3500 hd|\b3500\b|chey\s*3500|hd3500|silverao.*3500|1 ton 3500"),
        ("silverado 2500 hd", r"silverado.*2500|silverad.*2500|2500.*silverado|2500hd|2500 hd|\b2500\b|c\s*2500|ls\s*2500|cheyenne\s*2500"),
        ("silverado 1500", r"silverado|silverad|silverardo|sliverado|siverado|siliverado|si verado|si lverado|1500|trail boss|z\s*71|z71|high country|silver ltz"),
        ("express 3500", r"express.*3500|3500.*express|3500.*van|g3500"),
        ("express 2500", r"express.*2500|2500.*express|2500.*van|g2500"),
        ("express 1500", r"express.*1500|1500.*express"),
        ("express", r"express|expree|chevr exp|cargo van|conversion van|conversation van|g van|g series|\bg20\b|\bg30\b|workhourse"),
        ("s-10", r"\bs\s*10\b|\bs10\b"),
        ("aveo", r"aveo"),
        ("bolt ev", r"bolt ev|bolt"),
        ("volt", r"volt"),
        ("sonic", r"sonic|sinic|sonnic"),
        ("spark", r"spark"),
        ("trax", r"\btrax\b"),
        ("cruze", r"cruze|cruise|crusie|cruz"),
        ("cobalt", r"cobalt|coblat|colbalt"),
        ("cavalier", r"cavalier|calvier"),
        ("malibu", r"malibu|malibi|maibu"),
        ("impala", r"impala|imapla|impalla|imapa"),
        ("caprice", r"caprice"),
        ("ss", r"\bss\b"),
        ("camaro", r"camaro|comaro|camro|z28"),
        ("corvette", r"corvette|vette|\bc\s*[45]\b"),
        ("trailblazer", r"trailblazer|trail blazer|trailbalzer|trailblazee|trailblazser"),
        ("traverse", r"traverse|travers|treverse|travese|traversa|raverse"),
        ("equinox", r"equinox|eqinox"),
        ("blazer", r"blazer"),
        ("tahoe", r"tahoe|taho"),
        ("suburban", r"suburban|susburban"),
        ("avalanche", r"avalanche|avalance|avalache|alalanche"),
        ("colorado", r"colorado|colorad"),
        ("uplander", r"uplander|up lander"),
        ("venture", r"venture|venteur"),
        ("astro", r"astro|asto awd"),
        ("hhr", r"\bhhr\b"),
        ("monte carlo", r"monte carlo|\bmonte\b"),
        ("captiva sport", r"captiva|capitiva|capiva"),
        ("ssr", r"\bssr\b"),
        ("prizm", r"prizm|prism"),
        ("tracker", r"tracker"),
        ("lumina", r"lumina|lumima"),
        ("metro", r"\bmetro\b"),
        ("w-series or kodiak/n-series", r"(w\s*5500|w5500).*(isuzu|npr)|(isuzu|npr).*(w\s*5500|w5500)"),
        ("kodiak", r"kodiak|kodiack|topkick|top kick|c\s*4500|c4500|c\s*5500|c5500|c\s*6500|c6500|c\s*7500|c7500|c\s*8500|c8500|cc4500|cc5500|cc7h|w\s*4500|w4500|w\s*5500|w5500|tilt master|t5500|chevrolet3500|3500w|5500hd|g4500|\b4500\b|\b5500\b|\b6500\b|\b7500\b|\b8500\b"),
        ("c/k series", r"\bc\s*/?\s*k\s*2500\b|\bc\s*/?\s*k\s*3500\b|\bc2500\b|\bc3500\b|\bk2500\b|\bk3500\b|ck 2500|c10|c25|c35|chyenne|cheyenne|gmt\s*400|gmt-400|\bk series\b|\bp30\b"),
        ("beretta", r"beretta"),
        ("corsica", r"corsica"),
        ("bel air", r"belair|bel air"),
        ("chevelle", r"chevelle"),
        ("optra", r"optra"),
        ("avalanche", r"black diamond"),
        ("s-10", r"\bs\s*truck\b"),
        ("beretta", r"\bz\s*26\b|\bz26\b"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_toyota_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("prius prime", r"prius prime"),
        ("prius c", r"prius c"),
        ("prius v", r"prius v"),
        ("prius", r"prius|pruis|hybrid prius"),
        ("camry hybrid", r"camry hybrid"),
        ("camry solara", r"solara|salara"),
        ("camry", r"camry|camary|carmy|csmry|xamry|camr"),
        ("corolla hatchback", r"corolla hatchback"),
        ("corolla im", r"corolla im|\bim\b"),
        ("corolla", r"corolla|corrola|corrolla"),
        ("avalon hybrid", r"avalon hybrid"),
        ("avalon", r"avalon|avolon"),
        ("yaris ia", r"yaris ia"),
        ("yaris", r"yaris"),
        ("echo", r"echo"),
        ("matrix", r"matrix|martrix|matric|matris"),
        ("celica", r"celica"),
        ("supra", r"supra"),
        ("86", r"\b86\b|fr s|frs|gt86"),
        ("scion ia", r"scion ia"),
        ("scion iq", r"scion iq"),
        ("scion tc", r"scion tc"),
        ("scion xa", r"scion xa"),
        ("scion xb", r"scion xb|scion\+xb"),
        ("scion xd", r"scion xd"),
        ("sienna", r"sienna|seinna|sianna"),
        ("venza", r"venza|venva"),
        ("c-hr", r"c hr|chr"),
        ("rav4 hybrid", r"rav4 hybrid|rav 4 hybrid"),
        ("rav4", r"rav4|rav 4|\brav\b|rv4|rava"),
        ("highlander hybrid", r"highlander hybrid"),
        ("highlander", r"highlander|highlandr|highland xle|highlnader|higlander|hylander|hoghlander|\bhighl\b"),
        ("4runner", r"4runner|4 runner|forerunner|four runner"),
        ("sequoia", r"sequoia|sequia|sequioa"),
        ("land cruiser", r"land cruiser|landcruiser|land crusier"),
        ("fj cruiser", r"fj cruiser|fj crusier|\bfj\b"),
        ("tacoma", r"tacoma|tacom|tacome|taoma|tacpoma|pre runner|prerunner|trd pro"),
        ("tundra", r"tundra|tandra|tubdra"),
        ("pickup", r"\bpickup\b"),
        ("t100", r"\bt\s*100\b|\bt100\b"),
        ("mr2", r"\bmr\s*2\b|\bmr2\b"),
        ("previa", r"previa|privea"),
        ("tercel", r"tercel"),
        ("paseo", r"paseo"),
        ("hiace", r"hiace"),
        ("crown", r"\bcrown\b"),
        ("mirai", r"mirai"),
        ("hilux", r"hilux"),
        ("liteace", r"liteace"),
        ("estima", r"estima"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_honda_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("accord hybrid", r"accord hybrid"),
        ("accord crosstour", r"accord crosstour|crosstour"),
        ("accord", r"accord|accored"),
        ("civic hybrid", r"civic hybrid"),
        ("civic del sol", r"del sol"),
        ("civic", r"civic|cive|civi|civiv|civix"),
        ("clarity", r"clarity"),
        ("insight", r"insight"),
        ("fit", r"\bfit\b"),
        ("cr-z", r"cr z|crz"),
        ("s2000", r"s2000"),
        ("prelude", r"prelude"),
        ("integra", r"integra"),
        ("odyssey", r"odyssey|oddesey|oddessy|oddysey|oddyssey|odysee|odysey|odyssee|odyeesy"),
        ("pilot", r"pilot|piolt"),
        ("passport", r"passport"),
        ("ridgeline", r"ridgeline"),
        ("element", r"element"),
        ("hr-v", r"hr v|hrv"),
        ("cr-v", r"cr v|crv|cvr|rv v"),
        ("acty", r"acty"),
        ("gold wing", r"gold wing|goldwing"),
        ("cbr600rr", r"cbr\s*600rr|cbr600rr"),
        ("cbr650", r"cbr\s*650|cbr650"),
        ("vtx1300", r"vtx\s*1300|vtx1300"),
        ("vtx1800", r"vtx\s*1800|vtx1800"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_nissan_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("altima hybrid", r"altima hybrid"),
        ("altima", r"altima|alitma|altime|altma|atlima|sltima"),
        ("maxima", r"maxima|maxim|maximum|maxmia"),
        ("sentra", r"sentra|centra|seentra|senta"),
        ("versa note", r"versa note"),
        ("versa", r"versa"),
        ("leaf", r"leaf"),
        ("370z", r"370z"),
        ("350z", r"350z"),
        ("gt-r", r"gt r|gtr"),
        ("frontier", r"frontier|fromtier"),
        ("armada", r"armada|armanda"),
        ("titan xd", r"titan xd"),
        ("titan", r"titan"),
        ("xterra", r"xterra"),
        ("pathfinder", r"pathfinder|pathfider"),
        ("murano", r"murano|marano|maurano|morano|murrano"),
        ("rogue sport", r"rogue sport"),
        ("rogue", r"rogue"),
        ("kicks", r"kicks"),
        ("juke", r"juke"),
        ("cube", r"cube"),
        ("quest", r"quest"),
        ("nv3500", r"nv\s*3500|nv3500"),
        ("nv2500", r"nv\s*2500|nv2500"),
        ("nv200", r"nv\s*200|nv200"),
        ("nv1500", r"nv\s*1500|nv1500"),
        ("240sx", r"240sx"),
        ("300zx", r"300zx"),
        ("skyline", r"skyline"),
        ("note", r"\bnote\b"),
        ("vanette", r"vanette"),
        ("homy", r"\bhomy\b"),
        ("hardbody", r"hardbody|d21"),
        ("pickup", r"\bpickup\b|pickup truck"),
        ("z", r"\bz\b"),
        ("nv", r"\bnv\b"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_jeep_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("liberty", r"liberty|libert|library"),
        ("wrangler unlimited", r"wrangler unlimited|wrangler jk unlimited|wrangler jl unlimited|\bunlimited\b"),
        ("wrangler", r"wrangler|wranger|wranget|wrangkwr|wringler|wrnagler|rubicom|sahara|rio grande|rio grade|\btj\b|\byj\b|cj"),
        ("gladiator", r"gladiator|gladiaor"),
        ("grand cherokee l", r"grand cherokee\s+l\b"),
        ("grand cherokee", r"grand cherokee|grand charokee|grand cherkee|grand cherokke|\bzj\b|grand limited"),
        ("cherokee", r"cherokee|cherokree|cherooke|chrokee|\bxj\b"),
        ("compass", r"compass|compas"),
        ("patriot", r"patriot|partiot|patroit"),
        ("renegade", r"renegade"),
        ("commander", r"commander"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_ram_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("sprinter", r"sprinter"),
        ("promaster city", r"promaster city|pro master city"),
        ("promaster 3500", r"promaster.*3500|pro master.*3500"),
        ("promaster 2500", r"promaster.*2500|pro master.*2500"),
        ("promaster 1500", r"promaster.*1500|pro master.*1500"),
        ("promaster", r"promaster|pro master"),
        ("5500", r"\b5500\b|5500hd|ram5500"),
        ("4500", r"\b4500\b|4500hd"),
        ("3500", r"\b3500\b"),
        ("2500", r"\b2500\b|\b250\b"),
        ("2500", r"power wagon"),
        ("dakota", r"dakota|dakpta|dokota"),
        ("1500 classic", r"1500 classic"),
        ("1500", r"\b1500\b|rumblebee|\btrx\b"),
        ("c/v tradesman", r"c v tradesman|cv tradesman|\bcv\b|\bc v\b"),
        ("cargo van", r"cargo van"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_gmc_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("savana 3500", r"savana.*3500|savanna.*3500|savannah.*3500|3500.*savana"),
        ("savana 2500", r"savana.*2500|savanna.*2500|savannah.*2500|2500.*savana|g2500"),
        ("savana 1500", r"savana.*1500|1500.*savana"),
        ("savana", r"savana|savanna|savannah|savavna|sevanna|g3500|g3|vandura"),
        ("yukon xl", r"yukon xl|yukon denali xl|denali xl"),
        ("yukon", r"yukon|ykuon|yokon|yulon|\btahoe\b"),
        ("suburban", r"suburban"),
        ("acadia", r"acadia|arcadia"),
        ("topkick", r"topkick|top kick|kodiak|kodial|c\s*4500|c4500|c\s*5500|c5500|c\s*550o|c550o|c\s*6500|c6500|c\s*7500|c7500|c\s*8500|c8500|tc\s*4500|tc4500|tc5500|tc8500|tc75|c7h|t\s*6500|t6500|t\s*7500|t7500|t-?8500|\bc\s*series\b|\bc-series\b|\b4500\b|\b5500\b|\b6500\b|\b7500\b|\b8500\b"),
        ("sierra 3500 hd", r"sierra.*3500|3500.*sierra|3500hd|3500 hd|\b3500\b|c-?3500"),
        ("sierra 2500 hd", r"sierra.*2500|2500.*sierra|2500hd|2500 hd|\b2500\b|suburban\s*2500"),
        ("sierra 1500", r"sierra|seirra|serria|sieirra|1500"),
        ("canyon", r"canyon|cayon"),
        ("yukon xl", r"yukon xl|yukon denali xl"),
        ("yukon", r"yukon|ykuon|yokon|yulon"),
        ("terrain", r"terrain|terran|terrian|terrrain"),
        ("acadia", r"acadia|arcadia"),
        ("envoy xl", r"envoy xl"),
        ("envoy", r"envoy|evoy"),
        ("jimmy", r"jimmy"),
        ("safari", r"safari"),
        ("sonoma", r"sonoma|sanoma"),
        ("savana 3500", r"savana.*3500|savanna.*3500|savannah.*3500|3500.*savana"),
        ("savana 2500", r"savana.*2500|savanna.*2500|savannah.*2500|2500.*savana|g2500"),
        ("savana 1500", r"savana.*1500|1500.*savana"),
        ("savana", r"savana|savanna|savannah|savavna|sevanna|g3500|g3|vandura"),
        ("topkick", r"topkick|top kick|kodiak|kodial|c\s*4500|c4500|c\s*5500|c5500|c\s*6500|c6500|c\s*7500|c7500|c\s*8500|c8500|tc\s*4500|tc4500|tc5500|tc8500|tc75|c7h|t\s*6500|t6500|t\s*7500|t7500|t-?8500|\bc\s*series\b|\bc-series\b|\b4500\b|\b5500\b|\b6500\b|\b7500\b|\b8500\b"),
        ("w-series", r"\bw\s*4\b|\bw4\b|\bw\s*3500\b|\bw3500\b|\bw\s*4500\b|\bw4500\b|\bw\s*5500\b|\bw5500\b|ws\s*4500|cw5500"),
        ("c/k series", r"\bc\s*/?\s*k\s*2500\b|\bc\s*/?\s*k\s*3500\b|\bc2500\b|\bc3500\b|\bk3500\b"),
        ("suburban", r"suburban"),
        ("yukon", r"\btahoe\b"),
        ("sierra 1500", r"sportside|step side"),
        ("yukon xl", r"denali xl"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_bmw_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("1 series", r"\b1\s*series\b|\b128\b|\b128i\b|\b135\b|\b135i\b|\b135is\b"),
        ("2 series", r"\b2\s*series\b|\b228\b|\b228i\b|\b230i\b|\bm235\b|\bm235i\b|\b240m\b|\bm240i\b"),
        ("3 series", r"\b3\s*series\b|\b318\s*ti\b|\b318ti\b|\b320\b|\b320i\b|\b320xi\b|\b320x\s*drive\b|\b323\s*ci\b|\b323ci\b|\b323\s*i\b|\b325\b|\b325ci\b|\b325cic\b|\b325ic\b|\b325it\b|\b328\b|\b3281\b|\b328ci\b|\b328d\b|\b328gt\b|\b328xdrive\b|\b330\b|\b330ci\b|\b330cic\b|\b330e\b|\b330xi\b|\b3335xi\b|\b335\b|\b335d\b|\b335xi\b|\b340ix\b|\bm340xi\b|\b318i\b|\b323i\b|\b325i\b|\b328i\b|\b330i\b|\b335i\b|\b340i\b|\be46\b|bmw\s*325|bmw\s*328|bmw\s*330"),
        ("4 series", r"\b4\s*series\b|\b428\b|\b428i\b|\b430\b|\b430i\b|\b435\b|\b435i\b|\b440i\b|\b440xi\b|bmw\s*440"),
        ("5 series", r"\b5\b|\b5\s*series\b|\bactivehybrid\s*5\b|\b525\b|\b525ia\b|\b525xi\b|\b528\b|\b528xi\b|\b528ix\b|\b530\b|\b530e\b|\b530ia\b|\b530xi\b|\b530xit\b|\b535\b|\b535d\b|\b535gt\b|\b535ix\b|\b538i\b|\b540\b|\b550\b|\b550xi\b|\bm550\b|\bm550i\b|\b525i\b|\b528i\b|\b530i\b|\b535i\b|\b540i\b|\b545i\b|\b550i\b|bmw\s*525|bmw\s*528|bmw\s*530|bmw\s*535"),
        ("6 series", r"\b6\b|\b6\s*series\b|\b640\b|\b640i\b|\b645\s*ci\b|\b645ci\b|\b650ci\b|\b650xi\b|\b650i\b|6 convertible|bmw\s*650|alpina\s*b6"),
        ("7 series", r"\b7\s*series\b|\balpina\s*b7\b|\baplina\s*b7\b|\b725i\b|\b740\b|\b740e\b|\b740i\b|\b740li\b|\b740lxi\b|\b745\b|\b745i\b|\b745li\b|\b750\b|\b750i\b|\b750il\b|\b750l\b|\b750li\b|\b750lxi\b|\b750xi\b|\b760li\b|bmw\s*745|bmw\s*750"),
        ("8 series", r"\b8\s*series\b|\b840ci\b|\b840i\b|\b850ci\b|\b850i\b|\bm850i\b"),
        ("m2", r"\bm2\b"),
        ("m3", r"\bm3\b|\bm3cic\b"),
        ("m4", r"\bm4\b|\bm\s*4\b"),
        ("m5", r"\bm5\b"),
        ("m6", r"\bm6\b"),
        ("m8", r"\bm8\b"),
        ("m roadster", r"m roadster"),
        ("m coupe", r"m coupe"),
        ("x1", r"\bx1\b"),
        ("x2", r"\bx2\b"),
        ("x3 m", r"\bx3 m\b"),
        ("x3", r"\bx\s*-?\s*3\b|\bx3\b|x3si"),
        ("x4 m", r"\bx4 m\b"),
        ("x4", r"\bx4\b"),
        ("x5 m", r"\bx5 m\b"),
        ("x5", r"\bx\s*-?\s*5\b|\bx5\b|bmw\s*x5"),
        ("x6 m", r"\bx6 m\b"),
        ("x6", r"\bx6\b"),
        ("x7", r"\bx7\b"),
        ("z3", r"\bz\s*-?\s*3\b|\bz3\b|z3m"),
        ("z4", r"\bz4\b"),
        ("z8", r"\bz8\b"),
        ("i3", r"\bi3\b|bmwi3"),
        ("i4", r"\bi4\b"),
        ("i8", r"\bi8\b"),
        ("ix", r"\bix\b"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _normalize_dodge_model(value):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    patterns = [
        ("sprinter", r"sprinter"),
        ("grand caravan", r"grand caravan|grand carvan|grand can"),
        ("caravan", r"caravan"),
        ("durango", r"durango"),
        ("journey", r"journey|jorney|jouney"),
        ("nitro", r"nitro"),
        ("charger", r"charger|chager|charher"),
        ("challenger", r"challenger|challanger|challegner"),
        ("dart", r"\bdart\b"),
        ("avenger", r"avenger|advenger|avanger"),
        ("caliber", r"caliber|caliper|calliper"),
        ("magnum", r"magnum"),
        ("neon", r"neon"),
        ("stratus", r"stratus"),
        ("intrepid", r"intrepid"),
        ("viper", r"viper|srt 10"),
        ("ram 5500", r"ram.*5500|5500.*ram|5500hd|\b5500\b"),
        ("ram 3500", r"ram.*3500|3500.*ram|\b3500\b"),
        ("ram 2500", r"ram.*2500|2500.*ram|\b2500\b"),
        ("ram 1500", r"ram.*1500|1500.*ram|\b1500\b|dodge1500"),
        ("ram 4500", r"ram.*4500|4500.*ram|\b4500\b"),
        ("dakota", r"dakota|dakpta|dokota"),
        ("stealth", r"stealth"),
    ]
    match = _match_patterns(s, patterns)
    return match or _unknown(original)


ADDITIONAL_MODEL_PATTERNS = {
    "acura": [
        ("integra", r"integra"),
        ("rsx", r"\brsx\b"),
        ("tsx sport wagon", r"tsx.*wagon|wagon.*tsx"),
        ("tsx", r"\btsx\b"),
        ("tlx", r"\btlx\b"),
        ("tl", r"\btl\b|3\s*2tl"),
        ("rlx", r"\brlx\b"),
        ("rl", r"\brl\b|3\s*5rl"),
        ("ilx", r"\bilx\b"),
        ("zdx", r"\bzdx\b"),
        ("mdx", r"\bmdx\b"),
        ("rdx", r"\brdx\b"),
        ("cl", r"\bcl\b|3\s*0cl"),
        ("slx", r"\bslx\b"),
        ("nsx", r"\bnsx\b"),
    ],
    "alfa-romeo": [
        ("giulia", r"giulia"),
        ("stelvio", r"stelvio"),
        ("4c", r"\b4c\b"),
        ("spider", r"spider"),
        ("164", r"\b164\b"),
    ],
    "aston-martin": [
        ("dbx", r"\bdbx\b"),
        ("db11", r"\bdb11\b"),
        ("db9", r"\bdb9\b"),
        ("db7", r"\bdb7\b"),
        ("dbs", r"\bdbs\b"),
        ("vantage", r"vantage"),
        ("vanquish", r"vanquish"),
        ("rapide", r"rapide"),
    ],
    "audi": [
        ("e-tron gt", r"e tron gt|etron gt"),
        ("e-tron", r"e tron|etron"),
        ("rs q8", r"rs q8"),
        ("rs7", r"\brs\s*7\b|\brs7\b"),
        ("rs5", r"\brs\s*5\b|\brs5\b"),
        ("rs4", r"\brs\s*4\b|\brs4\b"),
        ("rs3", r"\brs\s*3\b|\brs3\b"),
        ("s8", r"\bs\s*8\b|\bs8\b"),
        ("s7", r"\bs\s*7\b|\bs7\b"),
        ("s6", r"\bs\s*6\b|\bs6\b"),
        ("s5", r"\bs\s*5\b|\bs5\b"),
        ("s4", r"\bs\s*4\b|\bs4\b"),
        ("s3", r"\bs\s*3\b|\bs3\b"),
        ("q8", r"\bq\s*8\b|\bq8\b"),
        ("q7", r"\bq\s*7\b|\bq7\b"),
        ("q5", r"\bq\s*5\b|\bq5\b"),
        ("q3", r"\bq\s*3\b|\bq3\b"),
        ("tts", r"\btts\b"),
        ("tt", r"\btt\b|tt1"),
        ("r8", r"\br\s*8\b|\br8\b"),
        ("a8", r"\ba\s*8\b|\ba8\b|a8l"),
        ("a7", r"\ba\s*7\b|\ba7\b"),
        ("a6", r"\ba\s*6\b|\ba6\b"),
        ("a5", r"\ba\s*5\b|\ba5\b"),
        ("a4 allroad", r"a4 allroad"),
        ("allroad", r"allroad"),
        ("a4", r"\ba\s*4\b|\ba4\b|a4quatro|ar quattro|avant quattro|avante quattro"),
        ("a3", r"\ba\s*3\b|\ba3\b"),
        ("sq5", r"\bsq\s*5\b|\bsq5\b"),
        ("rs6", r"\brs\s*6\b|\brs6\b"),
        ("100", r"\b100\b"),
    ],
    "bentley": [
        ("bentayga", r"bentayga"),
        ("continental gt", r"continental.*gt|gt.*continental|\bgt\b.*w12|w12.*\bgt\b"),
        ("continental flying spur", r"flying spur"),
        ("continental", r"continental"),
        ("mulsanne", r"mulsanne"),
        ("arnage", r"arnage"),
        ("azure", r"azure"),
    ],
    "buick": [
        ("encore gx", r"encore gx"),
        ("encore", r"encore"),
        ("envision", r"envision"),
        ("enclave", r"enclave|encalve|enlave|envlave"),
        ("regal tourx", r"regal tourx|tourx"),
        ("regal", r"regal"),
        ("lacrosse", r"lacrosse|la crosse|lacross|allure"),
        ("lucerne", r"lucerne|lecern|lecerne"),
        ("verano", r"verano|verao|verrano"),
        ("park avenue", r"park avenue"),
        ("lesabre", r"lesabre|le sabre|la sabre|lasabre|\besabre\b"),
        ("century", r"century|centry"),
        ("rendezvous", r"rendezvous|rendevous|renzendeous"),
        ("rainier", r"rainier|ranier|rainer"),
        ("terraza", r"terraza|terazza"),
        ("cascada", r"cascada"),
        ("riviera", r"riviera|rivera"),
        ("skylark", r"skylark"),
        ("park avenue", r"park ave|park avenue"),
        ("roadmaster", r"roadmaster"),
    ],
    "cadillac": [
        ("escalade ext", r"escalade ext"),
        ("escalade esv", r"escalade esv"),
        ("escalade", r"escalade|escalate"),
        ("escalade ext", r"\bext\b"),
        ("ct6", r"\bct\s*6\b|\bct6\b"),
        ("ct5", r"\bct\s*5\b|\bct5\b"),
        ("ct4", r"\bct\s*4\b|\bct4\b"),
        ("cts-v", r"cts v|ctsv"),
        ("cts", r"\bcts\b"),
        ("ats-v", r"ats v|atsv"),
        ("ats", r"\bats\b"),
        ("xt6", r"\bxt\s*6\b|\bxt6\b"),
        ("xt5", r"\bxt\s*5\b|\bxt5\b"),
        ("xt4", r"\bxt\s*4\b|\bxt4\b"),
        ("xts", r"\bxts\b"),
        ("deville", r"deville|de ville|devville"),
        ("seville", r"seville|sevile"),
        ("srx", r"\bsrx\b|\brxs\b"),
        ("sts", r"\bsts\b"),
        ("dts", r"\bdts\b|\bdtx\b|\bdhs\b"),
        ("sls", r"\bsls\b|northstar sls"),
        ("deville", r"deville|de ville|devville"),
        ("seville", r"seville|sevile"),
        ("eldorado", r"eldorado|eldorodo"),
        ("xlr", r"\bxlr\b"),
        ("elr", r"\belr\b"),
        ("allante", r"allante"),
        ("catera", r"catera"),
        ("fleetwood", r"fleetwood"),
    ],
    "chrysler": [
        ("300", r"\b300\b|300c"),
        ("200", r"\b200\b"),
        ("pt cruiser", r"pt cruiser|pt crusier|ptcruiser|p\s*t\s*cruiser"),
        ("sebring", r"sebring|serbring|serbing|seabring|\bjx\b"),
        ("town & country", r"town.*country|town.*county|town.*countr|tow.*country|towns.*cljnty|\bt\s*c\b|t&c"),
        ("pacifica", r"pacifica|pacific"),
        ("lebaron", r"lebaron|le baron"),
        ("concorde", r"concorde|concord"),
        ("lhs", r"\blhs\b"),
        ("cirrus", r"cirrus"),
        ("crossfire", r"crossfire"),
        ("aspen", r"aspen|aspin"),
        ("voyager", r"voyager"),
        ("prowler", r"prowler"),
    ],
    "eagle": [
        ("talon", r"talon"),
        ("summit", r"summit"),
        ("vision", r"vision"),
    ],
    "daimler": [
        ("super eight", r"super eight"),
        ("double six", r"double six"),
        ("six", r"\bsix\b"),
        ("xj", r"\bxj\b"),
    ],
    "fiat": [
        ("124 spider", r"124 spider|spider 124"),
        ("500x", r"\b500x\b"),
        ("500l", r"\b500l\b"),
        ("500e", r"\b500e\b"),
        ("500 abarth", r"500.*abarth|abarth.*500"),
        ("500", r"\b500\b|pop convertible"),
        ("freemont", r"freemont"),
    ],
    "ferrari": [
        ("f355", r"\bf\s*355\b|\bf355\b"),
        ("f50", r"\bf\s*50\b|\bf50\b"),
        ("ff", r"\bff\b"),
        ("812 superfast", r"812"),
        ("sf90", r"sf90"),
        ("roma", r"roma"),
        ("portofino", r"portofino"),
        ("f8", r"\bf8\b"),
        ("488", r"\b488\b"),
        ("458", r"\b458\b"),
        ("430", r"\b430\b|f430"),
        ("360", r"\b360\b"),
        ("california", r"california"),
        ("599", r"\b599\b"),
        ("575m", r"575"),
        ("550 maranello", r"550|maranello"),
        ("f12berlinetta", r"f12"),
    ],
    "fisker": [
        ("karma", r"karma"),
        ("ocean", r"ocean"),
    ],
    "freightliner": [
        ("m2", r"\bm\s*2\b|\bm2\b"),
        ("sprinter", r"sprinter"),
        ("fl70", r"\bfl\s*70\b|\bfl70\b"),
        ("columbia", r"columbia|colombia"),
    ],
    "gem": [
        ("e2", r"\be\s*2\b|\be2\b|e825"),
        ("e4", r"\be\s*4\b|\be4\b"),
        ("e6", r"\be\s*6\b|\be6\b"),
        ("el xd", r"\bel\s*xd\b|\belxd\b"),
        ("el", r"\bel\b"),
        ("es", r"\bes\b"),
        ("greengo", r"greengo"),
    ],
    "genesis": [
        ("gv80", r"\bgv\s*80\b|\bgv80\b"),
        ("gv70", r"\bgv\s*70\b|\bgv70\b"),
        ("g90", r"\bg\s*90\b|\bg90\b"),
        ("g80", r"\bg\s*80\b|\bg80\b"),
        ("g70", r"\bg\s*70\b|\bg70\b"),
        ("coupe", r"coupe"),
        ("sedan", r"\bgenesis\b.*\b(4\s*6|5\s*0)"),
        ("sedan", r"sedan"),
    ],
    "geo": [
        ("tracker", r"tracker"),
        ("metro", r"metro"),
        ("prizm", r"prizm|prism"),
        ("storm", r"storm"),
    ],
    "hummer": [
        ("h1", r"\bh\s*1\b|\bh1\b"),
        ("h2", r"\bh\s*2\b|\bh2\b|hummer\s*2"),
        ("h3t", r"\bh\s*3t\b|\bh3t\b"),
        ("h3", r"\bh\s*3\b|\bh3\b|hummer\s*3|h3x"),
    ],
    "hyundai": [
        ("g90", r"\bg\s*90\b|\bg90\b"),
        ("g80", r"\bg\s*80\b|\bg80\b"),
        ("g70", r"\bg\s*70\b|\bg70\b"),
        ("ioniq 5", r"ioniq 5"),
        ("ioniq", r"ioniq"),
        ("kona", r"kona"),
        ("palisade", r"palisade"),
        ("santa cruz", r"santa cruz"),
        ("santa fe", r"santa fe|sante fe|sant fe|snata fe"),
        ("tucson", r"tucson|tuscon|tuscan"),
        ("venue", r"venue"),
        ("veloster", r"veloster|velostor"),
        ("sonata hybrid", r"sonata hybrid"),
        ("sonata", r"sonata|sanota|sonota|sonat|sona\b"),
        ("elantra gt", r"elantra gt"),
        ("elantra", r"elantra|elanta|elentra|enlantra|elana yea"),
        ("accent", r"accent|aceent"),
        ("azera", r"azera"),
        ("equus", r"equus"),
        ("genesis coupe", r"genesis coupe"),
        ("genesis", r"genesis|genisis"),
        ("tiburon", r"tiburon"),
        ("xg350", r"xg350|xg300"),
        ("veracruz", r"veracruz"),
        ("nexo", r"nexo"),
        ("entourage", r"entourage"),
    ],
    "infiniti": [
        ("qx80", r"\bqx\s*80\b|\bqx80\b"),
        ("qx70", r"\bqx\s*70\b|\bqx70\b|\bfx\b|fx1|fx35|fx37|fx45|fx50"),
        ("qx60", r"\bqx\s*60\b|\bqx60\b|j35x|jx35|\bjx\b"),
        ("qx56", r"\bqx\s*56\b|\bqx56\b"),
        ("qx50", r"\bqx\s*50\b|\bqx50\b|ex35|ex37"),
        ("qx4", r"\bqx\s*4\b|\bqx4\b"),
        ("qx30", r"\bqx\s*30\b|\bqx30\b"),
        ("q70", r"\bq\s*70\b|\bq70\b|m35|m37|m45|m56"),
        ("q60", r"\bq\s*60\b|\bq60\b|g37 coupe"),
        ("q50", r"\bq\s*50\b|\bq50\b|g\s*25|g25|g\s*35|g35|g\s*37|g37|g sedan|g coupe|g convertible|g ipl"),
        ("q40", r"\bq\s*40\b|\bq40\b"),
        ("q45", r"\bq\s*45\b|\bq45\b"),
        ("i35", r"\bi35\b"),
        ("i30", r"\bi30\b"),
        ("g20", r"\bg\s*20\b|\bg20\b"),
    ],
    "isuzu": [
        ("ascender", r"ascender"),
        ("axiom", r"axiom"),
        ("rodeo sport", r"rodeo sport"),
        ("rodeo", r"rodeo"),
        ("trooper", r"trooper"),
        ("vehicross", r"vehicross"),
        ("hombre", r"hombre"),
        ("w-series", r"\bw\s*3500\b|\bw3500\b|\bw\s*4500\b|\bw4500\b|\bw\s*5500\b|\bw5500\b|w5500hd"),
        ("n-series", r"medium duty cabover|20ft.*box truck|ramp truck|dsl reg"),
        ("frr", r"\bfrr\b"),
        ("i-370", r"i\s*370|i370|i350"),
        ("i-290", r"i\s*290|i290"),
        ("npr", r"\bnpr\b|nph"),
        ("nqr", r"\bnqr\b"),
        ("nrr", r"\bnrr\b"),
        ("ftr", r"\bftr\b"),
        ("fvr", r"\bfvr\b"),
    ],
    "jaguar": [
        ("i-pace", r"i pace|ipace"),
        ("f-pace", r"f pace|fpace"),
        ("e-pace", r"e pace|epace"),
        ("f-type", r"f type|ftype"),
        ("x-type", r"x type|xtype"),
        ("s-type", r"s type|stype"),
        ("xe", r"\bxe\b"),
        ("xf", r"\bxf\b|xfr"),
        ("xj", r"\bxj\b|xj8|xjl|vanden plas|vandenplas|super v8"),
        ("xk", r"\bxk\b|xke|xk6"),
        ("xjr", r"\bxjr\b"),
        ("xkr", r"\bxkr\b"),
    ],
    "kia": [
        ("telluride", r"telluride"),
        ("stinger", r"stinger"),
        ("k5", r"\bk\s*5\b|\bk5\b"),
        ("k900", r"\bk\s*900\b|\bk900\b"),
        ("cadenza", r"cadenza"),
        ("forte koup", r"forte koup"),
        ("forte", r"forte"),
        ("rio", r"\brio\b"),
        ("soul ev", r"soul ev"),
        ("soul", r"soul|\bsol\b"),
        ("optima hybrid", r"optima hybrid"),
        ("optima", r"optima|optiam|optimia|optioma"),
        ("sorento", r"sorento|sorrento|sorent|sorent0|sorrnto"),
        ("sportage", r"sportage|sportgage|sportqage"),
        ("sedona", r"sedona|sodona"),
        ("niro", r"niro"),
        ("seltos", r"seltos"),
        ("amanti", r"amanti"),
        ("spectra", r"spectra"),
        ("sephia", r"sephia"),
        ("rondo", r"rondo"),
        ("borrego", r"borrego"),
    ],
    "lamborghini": [
        ("urus", r"urus"),
        ("huracan", r"huracan"),
        ("aventador", r"aventador"),
        ("gallardo", r"gallardo"),
        ("murcielago", r"murcielago"),
        ("diablo", r"diablo"),
    ],
    "land rover": [
        ("discovery sport", r"discovery sport"),
        ("discovery", r"discovery|discover\s*2"),
        ("lr4", r"\blr\s*4\b|\blr4\b"),
        ("lr3", r"\blr\s*3\b|\blr3\b"),
        ("lr2", r"\blr\s*2\b|\blr2\b"),
        ("range rover sport", r"range rover sport|range sport|sport hse|sport supercharged|sport 4wd|sport 4x4|sport\s*(3|au|die|hs|se|su|td|v6)|\bsport\b|\bspo\b"),
        ("range rover evoque", r"evoque|evoke"),
        ("range rover velar", r"velar"),
        ("range rover", r"range rover|rangerover|\brange\b|range hse|range diesel|autobiography|autobiog|supercharged|\bclassic\b|classic lwb|\blwb\b|county|l320|l322|hse|hse 4\.?6|4\.?6|4\s*6|td6|supercha|superchar"),
        ("discovery sport", r"discovery sport"),
        ("discovery", r"discovery|discover\s*2"),
        ("defender", r"defender"),
        ("lr4", r"\blr\s*4\b|\blr4\b"),
        ("lr3", r"\blr\s*3\b|\blr3\b"),
        ("lr2", r"\blr\s*2\b|\blr2\b"),
        ("freelander", r"freelander"),
    ],
    "lexus": [
        ("lc", r"\blc\b"),
        ("rc", r"\brc\b|rc200t|rc350|rcf"),
        ("ls", r"\bls\b|ls\s*400|ls\s*430|ls\s*460|ls\s*500|ls\s*600|ls600h"),
        ("gs", r"\bgs\b|gs\s*300|gs\s*350|gs\s*400|gs\s*430|gs\s*450|gs\s*460"),
        ("es", r"\bes\b|es\s*300|es\s*330|es\s*350"),
        ("is", r"\bis\b|is\s*200|is\s*250|is\s*300|is\s*350|isf|isc"),
        ("hs", r"\bhs\b|hs\s*250|hs250h"),
        ("ct", r"\bct\b|ct\s*200"),
        ("ux", r"\bux\b"),
        ("nx", r"\bnx\b|nx200t|nx300|nx300h"),
        ("rx", r"\brx\b|rx\s*300|rx\s*330|rx\s*350|rx\s*400|rx\s*450|rx30|rs\s*330"),
        ("gx", r"\bgx\b|gx\s*460|gx\s*470"),
        ("lx", r"\blx\b|lx\s*450|lx\s*470|lx\s*570|lx\s*600|lx740"),
        ("sc", r"\bsc\b|sc\s*300|sc\s*400|sc\s*430"),
    ],
    "lincoln": [
        ("navigator l", r"navigator l"),
        ("navigator", r"navigator"),
        ("aviator", r"aviator|aviatior"),
        ("nautilus", r"nautilus"),
        ("corsair", r"corsair"),
        ("mkx", r"\bmkx\b"),
        ("mkt", r"\bmkt\b"),
        ("mkc", r"\bmkc\b"),
        ("mks", r"\bmks\b"),
        ("mkz", r"\bmkz\b|zephyr"),
        ("continental", r"continental"),
        ("town car", r"town car|linc limo"),
        ("ls", r"\bls\b"),
        ("blackwood", r"blackwood"),
        ("mark viii", r"mark viii|mark 8|mark eight|mark vii"),
        ("mark lt", r"mark lt"),
    ],
    "lotus": [
        ("emira", r"emira"),
        ("evija", r"evija"),
        ("evora", r"evora"),
        ("exige", r"exige"),
        ("elise", r"elise"),
        ("esprit", r"esprit"),
        ("elan", r"elan"),
    ],
    "maserati": [
        ("levante", r"levante"),
        ("ghibli", r"ghibli"),
        ("quattroporte", r"quattroporte|quat+roporte"),
        ("granturismo", r"granturismo|gran turismo|randturismo"),
        ("grancabrio", r"grancabrio|gran cabrio"),
        ("coupe", r"\bcoupe\b"),
        ("spyder", r"spyder|sypder"),
    ],
    "maybach": [
        ("57s", r"\b57\s*s\b|\b57s\b"),
        ("57", r"\b57\b"),
        ("62s", r"\b62\s*s\b|\b62s\b"),
        ("62", r"\b62\b"),
    ],
    "mazda": [
        ("mx-5 miata", r"mx 5|mx5|miata"),
        ("mazdaspeed3", r"mazdaspeed3|mazda speed 3|speed\s*3"),
        ("mazdaspeed6", r"mazdaspeed6|mazda speed 6|speed\s*6"),
        ("cx-30", r"cx\s*30|cx30"),
        ("cx-9", r"cx\s*9|cx9"),
        ("cx-7", r"cx\s*7|cx7"),
        ("cx-5", r"cx\s*5|cx5"),
        ("cx-3", r"cx\s*3|cx3"),
        ("mazda2", r"mazda\s*2|mazda2|\b2\b|\b2 sport\b"),
        ("mazda3", r"mazda\s*3|mazda3|\b3\b|\b3\s+(grand touring|gt|hatchback|i|s|select|skyactiv|skyactive|sport|touring)|\b3i\b|\b3s\b|madza 3|mazada 3|mazdza3|\bm\s*3\b"),
        ("mazda5", r"mazda\s*5|mazda5|\b5\b|\b5\s+(grand touring|sport|touring|wagon|van)|\b5i sport\b|madza 5"),
        ("mazda6", r"mazda\s*6|mazda6|\b6\b|\b6\s+(grand touring|gt|i|s|sedan|sport|touring|wagon)|\b6i\b|6 2006|madza 6|mazd6"),
        ("cx-30", r"cx\s*30|cx30"),
        ("cx-9", r"cx\s*9|cx9"),
        ("cx-7", r"cx\s*7|cx7"),
        ("cx-5", r"cx\s*5|cx5"),
        ("cx-3", r"cx\s*3|cx3"),
        ("tribute", r"tribute|tribue"),
        ("protege5", r"protege\s*5|protege5|protégé 5|prot g 5"),
        ("protege", r"protege|protage|protoge"),
        ("millenia", r"millenia|mellenia|mallinia"),
        ("mpv", r"\bmpv\b|\bmvp\b"),
        ("rx-8", r"rx\s*8|rx8"),
        ("rx-7", r"rx\s*7|rx7"),
        ("626", r"\b626\b"),
        ("b-series", r"\bb\s*series\b|\bb\s*2300\b|\bb\s*2500\b|\bb\s*3000\b|\bb\s*4000\b|b400"),
        ("bongo", r"bongo"),
    ],
    "mercedes-benz": [
        ("g-class", r"\bg\s*class\b|\bg\s*wagen\b|\bg\s*500\b|\bg\s*550\b|\bg\s*55\b|\bg\s*63\b|\bg500\b|\bg550\b|\bg55\b|\bg63\b"),
        ("gls-class", r"\bgls\b|gls550"),
        ("gle-class", r"\bm\b|\bgle\b|gle350|\bm\s*class\b|\bml\b|\bml\s*250\b|\bml\s*320\b|\bml\s*350\b|\bml\s*430\b|\bml\s*450\b|\bml\s*500\b|\bml\s*550\b|\bml\s*55\b|\bml\s*63\b|\bml250\b|\bml320\b|\bml350\b|\bml430\b|\bml450\b|\bml500\b|\bml550\b|\bml55\b|\bml63\b|benz\s*m430"),
        ("glc-class", r"\bglc\b|glc300"),
        ("gla-class", r"\bgla\b|gla250"),
        ("glk-class", r"\bglk\b|glk250|glk350"),
        ("glb-class", r"\bglb\b|glb\s*250"),
        ("gl-class", r"\bgl\s*class\b|\bgl\b|\bgl\s*320\b|\bgl\s*350\b|\bgl\s*450\b|\bgl\s*550\b|\bgl320\b|\bgl350\b|\bgl450\b|\bgl550\b|450gl"),
        ("r-class", r"\br\s*class\b|\br\s*320\b|\br\s*350\b|\br\s*500\b|\br320\b|\br350\b|\br500\b"),
        ("cls-class", r"\bcls\b|cls500|cls55|cls63|cls\s*class"),
        ("s-class", r"\bs\b|\bs\s*class\b|s-clas|s\s*clas|\bs\s*320\b|\bs\s*350\b|\bs\s*400\b|\bs\s*420\b|\bs\s*430\b|\bs\s*450\b|\bs\s*500\b|\bs\s*550\b|\bs\s*560\b|\bs\s*600\b|\bs\s*55\b|\bs\s*63\b|\bs\s*65\b|\bs320\b|\bs350\b|\bs400\b|\bs420\b|\bs430\b|\bs450\b|\bs500\b|\bs550\b|\bs560\b|\bs600\b|\bs55\b|\bs63\b|\bs65\b|maybach\s*s560"),
        ("e-class", r"\be\b|\be\s*class\b|\be\s*250\b|\be\s*300\b|\be\s*320\b|\be\s*350\b|\be\s*400\b|\be\s*420\b|\be\s*430\b|\be\s*450\b|\be\s*500\b|\be\s*550\b|\be\s*55\b|\be\s*63\b|\be250\b|\be300\b|\be320\b|\be350\b|\be400\b|\be420\b|\be430\b|\be450\b|\be500\b|\be550\b|\be55\b|\be63|e5\s*50|e\s*43|e43|\b320e\b|benz\s*3e20|benz\s*e320w4"),
        ("c-class", r"\bc\b|\bc\s*class\b|\bc\s*220\b|\bc\s*230\b|\bc\s*240\b|\bc\s*250\b|\bc\s*280\b|\bc\s*300\b|\bc\s*320\b|\bc\s*350\b|\bc\s*400\b|\bc\s*43\b|\bc\s*450\b|\bc\s*55\b|\bc\s*63\b|\bc220\b|\bc230\b|\bc240\b|\bc250\b|\bc280\b|\bc300\b|\bc320\b|\bc350\b|\bc350e\b|\bc400\b|\bc43\b|\bc450\b|\bc55\b|\bc63\b|\bc63s\b|\bc32\b|\bc36\b|c 350e|benz\s*320\s*c"),
        ("a-class", r"\ba\s*class\b|\ba\s*220\b|\ba220\b"),
        ("b-class", r"\bb\s*class\b"),
        ("cla-class", r"\bcla\b|cla45"),
        ("clk-class", r"\bclk\b|clk\s*320|clk320|clk\s*350|clk350|clk\s*430|clk430|clk\s*500|clk500|clk\s*550|clk550|clk\s*55|clk55|benz\s*clx\s*430"),
        ("cl-class", r"\bcl\s*class\b|\bcl\s*55\b|\bcl\s*500\b|\bcl\s*550\b|\bcl\s*600\b|\bcl\s*63\b|\bcl55\b|\bcl500\b|\bcl550\b|\bcl600\b|\bcl63\b"),
        ("slk-class", r"\bslk\b|slk230|slk250|slk280|slk300|slk320|slk350|slk55|slk32"),
        ("slc-class", r"\bslc\b|slc300"),
        ("sl-class", r"\bsl\s*class\b|\bsl\b|\bsl\s*320\b|\bsl\s*400\b|\bsl\s*500\b|\bsl\s*550\b|\bsl\s*600\b|\bsl\s*55\b|\bsl\s*63\b|\bsl320\b|\bsl400\b|\bsl500\b|\bsl550\b|\bsl600\b|\bsl55\b|\bsl63\b|sl5pp|500sl"),
        ("sls amg", r"sls"),
        ("amg gt", r"amg gt"),
        ("sprinter", r"sprinter"),
        ("metris", r"metris"),
    ],
    "mercury": [
        ("grand marquis", r"grand marquis|\bmarquis\b"),
        ("marauder", r"marauder"),
        ("montego", r"montego"),
        ("milan", r"milan"),
        ("sable", r"sable"),
        ("cougar", r"cougar"),
        ("mystique", r"mystique"),
        ("mountaineer", r"mountaineer|mountainner|moutaineer"),
        ("mariner", r"mariner|marineer|marinr"),
        ("monterey", r"monterey"),
        ("villager", r"villager"),
    ],
    "mini": [
        ("cooper countryman", r"countryman"),
        ("cooper clubman", r"clubman"),
        ("cooper paceman", r"paceman"),
        ("cooper coupe", r"\bcoupe\b"),
        ("cooper roadster", r"roadster"),
        ("cooper convertible", r"convertible"),
        ("cooper hardtop", r"hardtop"),
        ("cooper", r"cooper|coooper|copper"),
    ],
    "mitsubishi": [
        ("outlander sport", r"outlander sport"),
        ("outlander phev", r"outlander phev"),
        ("outlander", r"outlander"),
        ("eclipse cross", r"eclipse cross"),
        ("eclipse", r"eclipse"),
        ("lancer evolution", r"lancer evolution|evolution|evo"),
        ("lancer", r"lancer"),
        ("mirage g4", r"mirage g4"),
        ("mirage", r"mirage"),
        ("galant", r"galant"),
        ("endeavor", r"endeavor"),
        ("montero sport", r"montero sport"),
        ("montero", r"montero|monteri|pajero"),
        ("diamante", r"diamante"),
        ("raider", r"raider"),
        ("3000gt", r"3000\s*gt|3000gt"),
        ("i-miev", r"i miev|imiev|\bmiev\b"),
        ("fuso", r"fuso|fusco|fe\s*140|fe\s*160|fe\s*180|fk\s*260"),
        ("delica", r"delica"),
        ("minicab", r"mini cab|mini-cab"),
    ],
    "morgan": [
        ("plus four", r"plus four|\b4 4\b"),
        ("plus eight", r"plus eight|plus 8"),
        ("aero 8", r"aero 8"),
        ("3 wheeler", r"3 wheeler|three wheeler"),
    ],
    "oldsmobile": [
        ("alero", r"alero"),
        ("aurora", r"aurora"),
        ("bravada", r"bravada|bradvo"),
        ("intrigue", r"intrigue"),
        ("cutlass", r"cutlass"),
        ("lss", r"\blss\b"),
        ("regency", r"regency"),
        ("eighty-eight", r"eighty eight|88"),
        ("ninety-eight", r"ninety eight|98"),
        ("silhouette", r"silhouette|silhoutte|silouette"),
        ("achieva", r"achieva"),
    ],
    "plymouth": [
        ("prowler", r"prowler"),
        ("breeze", r"breeze"),
        ("neon", r"neon"),
        ("voyager", r"voyager"),
        ("grand voyager", r"grand voyager"),
    ],
    "pontiac": [
        ("g8", r"\bg\s*8\b|\bg8\b|g8gt"),
        ("g6", r"\bg\s*6\b|\bg6\b|pontiacg6"),
        ("g5", r"\bg\s*5\b|\bg5\b"),
        ("g3", r"\bg\s*3\b|\bg3\b"),
        ("solstice", r"solstice|solistice|soltice"),
        ("vibe", r"vibe"),
        ("torrent", r"torrent"),
        ("aztek", r"aztek|aztec"),
        ("grand prix", r"grand prix|gr prix"),
        ("grand am", r"grand am"),
        ("bonneville", r"bonneville|boneville"),
        ("firebird", r"firebird|trans am"),
        ("sunfire", r"sunfire"),
        ("montana", r"montana|montanna"),
        ("gto", r"\bgto\b"),
        ("trans sport", r"trans sport"),
    ],
    "porsche": [
        ("taycan", r"taycan"),
        ("panamera", r"panamera"),
        ("macan", r"macan"),
        ("cayenne", r"cayenne|caynne"),
        ("718 boxster", r"718.*boxster"),
        ("718 cayman", r"718.*cayman"),
        ("718", r"\b718\b"),
        ("boxster", r"boxster|boxter|\b986\b"),
        ("cayman", r"cayman"),
        ("911", r"\b911\b|\b996\b|\b997\b|carrera|targa|turbo s|\bgt3\b"),
        ("968", r"\b968\b"),
        ("928", r"\b928\b"),
    ],
    "rover": [
        ("discovery sport", r"discovery sport"),
        ("discovery", r"discovery|discover 2"),
        ("lr4", r"\blr\s*4\b|\blr4\b"),
        ("lr3", r"\blr\s*3\b|\blr3\b"),
        ("lr2", r"\blr\s*2\b|\blr2\b"),
        ("range rover sport", r"range rover sport|range sport|sport hse|sport supercharged|sport 4wd|sport 4x4|sport\s*(3|au|die|hs|se|su|td|v6)|\bsport\b"),
        ("range rover evoque", r"evoque|evoke"),
        ("range rover velar", r"velar"),
        ("range rover", r"range rover|rangerover|range hse|range diesel|autobiography|autobiog|supercharged|classic lwb|county|l320|l322|hse|hse 4\.?6|4\.?6|4\s*6|td6|supercha|superchar"),
        ("discovery sport", r"discovery sport"),
        ("discovery", r"discovery|discover 2"),
        ("defender", r"defender"),
        ("lr4", r"\blr\s*4\b|\blr4\b"),
        ("lr3", r"\blr\s*3\b|\blr3\b"),
        ("lr2", r"\blr\s*2\b|\blr2\b"),
        ("freelander", r"freelander"),
    ],
    "rolls-royce": [
        ("phantom", r"phantom"),
        ("ghost", r"ghost"),
        ("wraith", r"wraith"),
        ("dawn", r"\bdawn\b"),
        ("cullinan", r"cullinan"),
        ("silver seraph", r"silver seraph"),
        ("silver spur", r"silver spur"),
        ("silver dawn", r"silver dawn"),
    ],
    "saab": [
        ("9000", r"\b9000\b"),
        ("900", r"\b900\b"),
        ("9-7x", r"9\s*7x|97x"),
        ("9-5", r"9\s*5|95"),
        ("9-4x", r"9\s*4x|94x"),
        ("9-3", r"9\s*3|93|convertible"),
        ("9-2x", r"9\s*2x|92x"),
    ],
    "saturn": [
        ("outlook", r"outlook|aoutlok"),
        ("vue", r"\bvue\b|\bvuw\b"),
        ("aura", r"aura|auru"),
        ("ion", r"\bion\b"),
        ("astra", r"astra"),
        ("sky", r"\bsky\b"),
        ("relay", r"relay"),
        ("l-series", r"\bl\s*series\b|\bl\s*-?\s*100\b|\bl100\b|\bl\s*-?\s*200\b|\bl200\b|\bl\s*-?\s*300\b|\bl300\b|\bls300\b|\blw200\b|\blw300\b|\bls\b|\bls2\b"),
        ("s-series", r"\bs\s*series\b|\bsl\b|\bsl1\b|\bsl2\b|\bsc\b|\bsc1\b|\bsc2\b|\bsw\b|\bsw2\b"),
    ],
    "scion": [
        ("fr-s", r"fr s|frs"),
        ("ia", r"\bia\b"),
        ("im", r"\bim\b"),
        ("iq", r"\biq\b"),
        ("tc", r"\btc\b|tcscion"),
        ("xa", r"\bxa\b"),
        ("xb", r"\bxb\b"),
        ("xd", r"\bxd\b"),
    ],
    "smart": [
        ("fortwo electric drive", r"fortwo.*electric|electric.*fortwo|electric drive prime"),
        ("fortwo", r"fortwo|for two|smart car|smartcar|passion"),
    ],
    "subaru": [
        ("wrx sti", r"wrx sti|sti"),
        ("wrx", r"\bwrx\b"),
        ("brz", r"\bbrz\b"),
        ("tribeca", r"\bb\s*9\b|\bb9\b"),
        ("ascent", r"ascent"),
        ("crosstrek", r"crosstrek|cross trek"),
        ("xv crosstrek", r"xv"),
        ("forester", r"forester|foreser|forestor|foreter|forster"),
        ("outback", r"outback|outbback|putback"),
        ("legacy", r"legacy"),
        ("impreza", r"impreza|impeza|imprezza|inpreza"),
        ("tribeca", r"tribeca|tribecca|triveca"),
        ("baja", r"baja"),
    ],
    "suzuki": [
        ("equator", r"equator"),
        ("kizashi", r"kizashi"),
        ("sx4", r"\bsx\s*4\b|\bsx4\b"),
        ("xl7", r"\bxl\s*7\b|\bxl7\b"),
        ("grand vitara", r"grand vitara"),
        ("vitara", r"vitara|vitera"),
        ("aerio", r"aerio"),
        ("esteem", r"esteem"),
        ("forenza", r"forenza|firenza"),
        ("reno", r"\breno\b"),
        ("samurai", r"samurai"),
        ("sidekick", r"sidekick"),
        ("carry", r"carry"),
        ("wagon r", r"wagon r"),
        ("gw250", r"gw250"),
        ("vl800", r"vl800"),
        ("vl1500", r"vl1500"),
        ("gsx-r600", r"gsx r600|gsx-r600"),
        ("gsx-r750", r"gsx r750|gsx-r750"),
        ("gsx-s750", r"gsx s750|gsx-s750"),
        ("gsx1300r", r"gsx1300r"),
        ("sfv650", r"sfv650"),
    ],
    "tesla": [
        ("model y", r"model y"),
        ("model y", r"\by performance\b"),
        ("model 3", r"model 3|\b3\b"),
        ("model x", r"model x"),
        ("model s", r"model s|modle s|model 60s|s model|\bs\b|\bs\s*(75|85|90d|p85|p90d|p100d)"),
        ("roadster", r"roadster"),
    ],
    "volkswagen": [
        ("atlas cross sport", r"atlas cross sport"),
        ("atlas", r"atlas"),
        ("arteon", r"arteon"),
        ("e-golf", r"e golf|egolf"),
        ("golf alltrack", r"golf alltrack|alltrack"),
        ("golf sportwagen", r"sportwagen|sport wagon"),
        ("golf gti", r"\bgti\b|golf gti"),
        ("golf r", r"golf r"),
        ("golf", r"golf|rabbit"),
        ("jetta gli", r"jetta gli|\bgli\b"),
        ("jetta sportwagen", r"jetta sportwagen"),
        ("jetta", r"jetta|jeeta|mk4 ute"),
        ("passat", r"passat|passsat"),
        ("beetle", r"beetle|beelte|bettle|bug|new beetle"),
        ("tiguan", r"tiguan|tijuan"),
        ("touareg", r"touareg|toureg"),
        ("id.4", r"id\s*4|id4"),
        ("cc", r"\bcc\b"),
        ("eos", r"eos"),
        ("cabrio", r"cabrio|cabriolet"),
        ("r32", r"\br\s*32\b|\br32\b"),
        ("phaeton", r"phaeton"),
        ("routan", r"routan|routen"),
        ("eurovan", r"eurovan|euro van"),
    ],
    "volvo": [
        ("xc90", r"\bxc\s*90\b|\bxc90\b"),
        ("xc70", r"\bxc\s*70\b|\bxc70\b"),
        ("xc60", r"\bxc\s*60\b|\bxc60\b|cx\s*60"),
        ("xc40", r"\bxc\s*40\b|\bxc40\b"),
        ("c70", r"\bc\s*70\b|\bc70\b"),
        ("c30", r"\bc\s*30\b|\bc30\b"),
        ("s90", r"\bs\s*90\b|\bs90\b"),
        ("s80", r"\bs\s*80\b|\bs80\b"),
        ("s70", r"\bs\s*70\b|\bs70\b"),
        ("s60", r"\bs\s*60\b|\bs60\b|60\s*t\s*5"),
        ("s40", r"\bs\s*40\b|\bs40\b"),
        ("v90", r"\bv\s*90\b|\bv90\b"),
        ("v70", r"\bv\s*70\b|\bv70\b"),
        ("v60", r"\bv\s*60\b|\bv60\b"),
        ("v50", r"\bv\s*50\b|\bv50\b"),
        ("v40", r"\bv\s*40\b|\bv40\b"),
        ("960", r"\b960\b"),
        ("940", r"\b940\b"),
        ("vnl", r"\bvnl\b|vnl\s*670|vnl64t670"),
        ("vnm", r"\bvnm\b|vnm\s*64t200|vnm200"),
        ("850", r"\b850\b"),
        ("xc70", r"cross country"),
    ],
}


_DETAILED_MODEL_NAMES = {
    "ford": [
        "f-59 stripped chassis",
        "f-800",
        "f-750",
        "f-650",
        "f-550 super duty",
        "f-450 super duty",
        "f-350 super duty",
        "f-250 super duty",
        "f-150",
        "e-150",
        "e-250",
        "e-350",
        "e-450",
        "e-series / econoline",
        "transit connect",
        "transit 150",
        "transit 250",
        "transit 350",
        "transit",
        "explorer sport trac",
        "expedition max",
        "expedition el",
        "fusion energi",
        "fusion hybrid",
        "c-max energi",
        "c-max hybrid",
        "taurus x",
        "crown victoria",
        "ranger",
        "bronco",
        "ecosport",
        "escape",
        "edge",
        "explorer",
        "expedition",
        "excursion",
        "flex",
        "mustang",
        "thunderbird",
        "focus",
        "escort",
        "contour",
        "fiesta",
        "fusion",
        "taurus",
        "five hundred",
        "freestyle",
        "freestar",
        "windstar",
    ],
    "chevrolet": [
        "silverado 3500 hd",
        "silverado 2500 hd",
        "silverado 1500",
        "express 3500",
        "express 2500",
        "express 1500",
        "express",
        "s-10",
        "aveo",
        "bolt ev",
        "volt",
        "sonic",
        "spark",
        "cruze",
        "cobalt",
        "cavalier",
        "malibu",
        "impala",
        "caprice",
        "ss",
        "camaro",
        "corvette",
        "trailblazer",
        "traverse",
        "equinox",
        "blazer",
        "tahoe",
        "suburban",
        "avalanche",
        "colorado",
        "uplander",
        "venture",
        "astro",
        "hhr",
        "monte carlo",
        "prizm",
        "tracker",
    ],
    "toyota": [
        "prius prime",
        "prius c",
        "prius v",
        "prius",
        "camry hybrid",
        "camry solara",
        "camry",
        "corolla hatchback",
        "corolla im",
        "corolla",
        "avalon hybrid",
        "avalon",
        "yaris ia",
        "yaris",
        "echo",
        "matrix",
        "celica",
        "supra",
        "86",
        "sienna",
        "venza",
        "c-hr",
        "rav4 hybrid",
        "rav4",
        "highlander hybrid",
        "highlander",
        "4runner",
        "sequoia",
        "land cruiser",
        "fj cruiser",
        "tacoma",
        "tundra",
    ],
    "honda": [
        "accord hybrid",
        "accord crosstour",
        "accord",
        "civic hybrid",
        "civic del sol",
        "civic",
        "clarity",
        "insight",
        "fit",
        "cr-z",
        "s2000",
        "prelude",
        "odyssey",
        "pilot",
        "passport",
        "ridgeline",
        "element",
        "hr-v",
        "cr-v",
    ],
    "nissan": [
        "altima hybrid",
        "altima",
        "maxima",
        "sentra",
        "versa note",
        "versa",
        "leaf",
        "370z",
        "350z",
        "gt-r",
        "frontier",
        "titan xd",
        "titan",
        "xterra",
        "pathfinder",
        "armada",
        "murano",
        "rogue sport",
        "rogue",
        "kicks",
        "juke",
        "cube",
        "quest",
        "nv3500",
        "nv2500",
        "nv200",
        "nv",
    ],
    "jeep": [
        "wrangler unlimited",
        "wrangler",
        "gladiator",
        "grand cherokee l",
        "grand cherokee",
        "cherokee",
        "compass",
        "patriot",
        "renegade",
        "commander",
        "liberty",
    ],
    "ram": [
        "promaster city",
        "promaster 3500",
        "promaster 2500",
        "promaster 1500",
        "promaster",
        "3500",
        "2500",
        "1500 classic",
        "1500",
        "dakota",
        "c/v tradesman",
        "cargo van",
    ],
    "gmc": [
        "sierra 3500 hd",
        "sierra 2500 hd",
        "sierra 1500",
        "canyon",
        "yukon xl",
        "yukon",
        "terrain",
        "acadia",
        "envoy xl",
        "envoy",
        "jimmy",
        "safari",
        "sonoma",
        "savana 3500",
        "savana 2500",
        "savana 1500",
        "savana",
    ],
    "bmw": [
        "1 series",
        "2 series",
        "3 series",
        "4 series",
        "5 series",
        "6 series",
        "7 series",
        "8 series",
        "m2",
        "m3",
        "m4",
        "m5",
        "m6",
        "m8",
        "x1",
        "x2",
        "x3 m",
        "x3",
        "x4 m",
        "x4",
        "x5 m",
        "x5",
        "x6 m",
        "x6",
        "x7",
        "z3",
        "z4",
        "z8",
        "i3",
        "i4",
        "i8",
        "ix",
    ],
    "dodge": [
        "grand caravan",
        "caravan",
        "durango",
        "journey",
        "nitro",
        "charger",
        "challenger",
        "dart",
        "avenger",
        "caliber",
        "magnum",
        "neon",
        "stratus",
        "intrepid",
        "viper",
        "ram 3500",
        "ram 2500",
        "ram 1500",
        "dakota",
    ],
}


def _build_model_to_manufacturer():
    model_to_manufacturers = {}

    for manufacturer, model_names in _DETAILED_MODEL_NAMES.items():
        for model_name in model_names:
            model_to_manufacturers.setdefault(model_name, set()).add(manufacturer)

    for manufacturer, patterns in ADDITIONAL_MODEL_PATTERNS.items():
        for model_name, _ in patterns:
            model_to_manufacturers.setdefault(model_name, set()).add(manufacturer)

    return {
        model_name: next(iter(manufacturers))
        for model_name, manufacturers in model_to_manufacturers.items()
        if len(manufacturers) == 1
    }


MODEL_TO_MANUFACTURER = _build_model_to_manufacturer()


_MODEL_ALIAS_OVERRIDES = {
    "3 series": ["323i", "325 xi", "325xi", "328 i", "328i", "328is", "328xi", "335i", "335i xdrive"],
    "5 series": ["535xi", "535xi premium sport"],
    "7 series": ["740il"],
    "accord": ["acord"],
    "altima": ["altimae"],
    "avalanche": ["avalanch", "avalance north face", "avanlanche"],
    "aveo": ["aveo"],
    "camaro": ["camero", "z28"],
    "camry": ["camery", "camrey", "fakery"],
    "c-class": ["c230", "c 230"],
    "cavalier": ["caviler", "cavlier"],
    "challenger": ["chalenger"],
    "cherokee": ["cheroke"],
    "civic": ["civc", "civics"],
    "cooper clubman": ["clubman", "clubman s"],
    "colorado": ["colardo"],
    "concorde": ["concord"],
    "corolla": ["carolla", "corola"],
    "corvette": ["corevette", "corvet", "vette", "z06"],
    "crown victoria": ["crown vic", "p71", "police interceptor p71"],
    "cr-v": ["crv", "cr v"],
    "crosstrek": ["cross trek"],
    "cruze": ["cruse"],
    "cla-class": ["cla250", "cla 250"],
    "cls-class": ["cls550", "cls 550"],
    "durango": ["durang"],
    "e-class": ["e 320 wagon", "e63s", "e63s amg"],
    "e-150": ["e150", "e 150"],
    "e-250": ["e250", "e 250"],
    "e-350": ["e350", "e 350"],
    "e-450": ["e450", "e 450"],
    "eclipse": ["eclipes"],
    "elantra": ["elentra"],
    "es": ["es330", "es 330", "es350", "es 350"],
    "escalade": ["escaladee"],
    "escort": ["zx2"],
    "expedition": ["expedici n"],
    "explorer": ["explore"],
    "f-150": ["f150", "f 150", "f150xl", "f l50", "f15o", "f 15o", "fx 4 crew cab f15o", "svt raptor", "raptor"],
    "f-250 super duty": ["f250", "f 250", "f25o", "f 25o", "super duty f 250", "superduty f25o"],
    "f-350 super duty": ["f350", "f 350", "super duty f 350"],
    "f-450 super duty": ["f450", "f 450"],
    "f-550 super duty": ["f550", "f 550"],
    "f-800": ["f800", "f8oo", "f 8oo"],
    "firebird": ["trans am", "firehawk"],
    "fiesta": ["feista"],
    "forester": ["forrester"],
    "fusion": ["fusiom", "fussion"],
    "grand cherokee": ["grand cheroke"],
    "gle-class": ["m class", "ml320", "ml 320", "ml350", "ml 350", "ml350 bluetec"],
    "highlander": ["high lander"],
    "huracan": ["huracan", "hurracan"],
    "i-miev": ["miev"],
    "jetta": ["jeta", "yetta"],
    "land cruiser": ["landcruiser"],
    "lancer evolution": ["evo x"],
    "malibu": ["mailbu"],
    "mark viii": ["mark 8", "mark8"],
    "montero": ["montaro"],
    "mx-5 miata": ["miata"],
    "mustang": ["mustng", "cobra"],
    "odyssey": ["odessey", "odessy"],
    "outback": ["outbak", "outack"],
    "panamera": ["panemera"],
    "passat": ["passet"],
    "pathfinder": ["path finder"],
    "pilot": ["piolet"],
    "prius": ["prious"],
    "q50": ["g25x", "g35", "g35 sport coupe", "g37s", "g37x"],
    "q70": ["m35", "m37x", "m56x"],
    "qx50": ["ex35"],
    "qx70": ["fx45", "fx fx45"],
    "rav4": ["rav 4", "rave4"],
    "rav4 hybrid": ["rav 4 hybrid"],
    "ridgeline": ["ridge line", "ridheline"],
    "rogue": ["rouge"],
    "sierra 1500": ["ciera", "cierra", "sierra", "gas sierra", "sierra denali"],
    "silverado 1500": ["silverado", "silverado1500", "silverado 15oo"],
    "silverado 2500 hd": ["silverado2500hd", "silverado 2500hd", "silverado 2500 hd"],
    "silverado 3500 hd": ["silverado3500hd", "silverado 3500hd", "silverado 3500 hd"],
    "santa fe": ["sante fe"],
    "sl-class": ["sl400", "sl 400", "sl600", "sl 600"],
    "slk-class": ["slk230"],
    "sonata": ["sanata", "sanota"],
    "tacoma": ["tocoma"],
    "taurus": ["turus", "p7b", "police interceptor p7b"],
    "tiguan": ["tiquan"],
    "town & country": ["town and country", "town country"],
    "transit connect": ["ransit connect"],
    "tucson": ["tuscon"],
    "tundra": ["tundra"],
    "wrangler": ["rangler", "wangler", "yj", "rubicon"],
    "wrx sti": ["sti"],
    "x5": ["x5m"],
    "xj": ["xj6", "xjs"],
    "xk": ["xk8"],
    "xterra": ["exterra"],
    "yukon": ["yuklon"],
}


def _build_model_aliases():
    aliases_by_model = {}

    for model_name in MODEL_TO_MANUFACTURER:
        aliases = {model_name}
        aliases.add(model_name.replace("-", " "))
        aliases.add(model_name.replace("-", ""))
        aliases.add(model_name.replace(" ", ""))
        aliases.add(re.sub(r"[^a-z0-9]+", " ", model_name).strip())
        aliases.add(re.sub(r"[^a-z0-9]+", "", model_name))
        aliases.update(_MODEL_ALIAS_OVERRIDES.get(model_name, []))

        aliases_by_model[model_name] = sorted(alias for alias in aliases if alias)

    return aliases_by_model


MODEL_ALIASES = _build_model_aliases()


def _alias_pattern(alias):
    cleaned_alias, _ = _clean_value(alias)
    parts = cleaned_alias.split()
    return r"\b" + r"\s+".join(map(re.escape, parts)) + r"\b"


MODEL_ALIAS_PATTERNS = [
    (model_name, _alias_pattern(alias))
    for model_name, aliases in MODEL_ALIASES.items()
    for alias in aliases
]

COMPACT_MODEL_ALIASES = [
    (model_name, re.sub(r"[^a-z0-9]+", "", alias.lower()))
    for model_name, aliases in MODEL_ALIASES.items()
    for alias in aliases
]


_MODEL_ALIAS_MATCH_OVERRIDES = [
    ("jaguar", "xj", ["xj6", "xjs"]),
    ("lexus", "es", ["es 330", "es330", "es 350", "es350"]),
]


_MODEL_ALIAS_MATCH_OVERRIDE_PATTERNS = [
    (manufacturer, model_name, _alias_pattern(alias))
    for manufacturer, model_name, aliases in _MODEL_ALIAS_MATCH_OVERRIDES
    for alias in aliases
]


_COMPACT_MODEL_ALIAS_MATCH_OVERRIDES = [
    (manufacturer, model_name, re.sub(r"[^a-z0-9]+", "", alias.lower()))
    for manufacturer, model_name, aliases in _MODEL_ALIAS_MATCH_OVERRIDES
    for alias in aliases
]


def _match_model_alias(value, expected_manufacturer=None):
    s, _ = _clean_value(value)
    if s is None:
        return None, None

    for model_name, pattern in MODEL_ALIAS_PATTERNS:
        manufacturer = MODEL_TO_MANUFACTURER[model_name]
        if expected_manufacturer in (None, manufacturer) and re.search(pattern, s):
            return manufacturer, model_name

    for manufacturer, model_name, pattern in _MODEL_ALIAS_MATCH_OVERRIDE_PATTERNS:
        if expected_manufacturer in (None, manufacturer) and re.search(pattern, s):
            return manufacturer, model_name

    compact_model = re.sub(r"[^a-z0-9]+", "", s)
    for model_name, compact_alias in COMPACT_MODEL_ALIASES:
        manufacturer = MODEL_TO_MANUFACTURER[model_name]
        if (
            expected_manufacturer in (None, manufacturer)
            and len(compact_alias) >= 3
            and compact_alias in compact_model
        ):
            return manufacturer, model_name

    for manufacturer, model_name, compact_alias in _COMPACT_MODEL_ALIAS_MATCH_OVERRIDES:
        if (
            expected_manufacturer in (None, manufacturer)
            and len(compact_alias) >= 3
            and compact_alias in compact_model
        ):
            return manufacturer, model_name

    return None, None


def _normalize_with_patterns(value, patterns):
    s, original = _clean_value(value)
    if s is None:
        return _unknown(original)

    match = _match_patterns(s, patterns)
    return match or _unknown(original)


def _make_pattern_normalizer(manufacturer):
    def normalize(value):
        return _normalize_with_patterns(value, ADDITIONAL_MODEL_PATTERNS[manufacturer])

    return normalize


MODEL_NORMALIZERS = {
    "ford": _normalize_ford_model,
    "chevrolet": _normalize_chevrolet_model,
    "toyota": _normalize_toyota_model,
    "honda": _normalize_honda_model,
    "nissan": _normalize_nissan_model,
    "jeep": _normalize_jeep_model,
    "ram": _normalize_ram_model,
    "gmc": _normalize_gmc_model,
    "bmw": _normalize_bmw_model,
    "dodge": _normalize_dodge_model,
}

MODEL_NORMALIZERS.update(
    {
        manufacturer: _make_pattern_normalizer(manufacturer)
        for manufacturer in ADDITIONAL_MODEL_PATTERNS
    }
)


MANUFACTURER_ALIASES = {
    "acura": ["acura", "accura", "akura"],
    "alfa-romeo": ["alfa-romeo", "alfa romeo", "alpha-romeo", "alpha romeo", "alfa"],
    "aston-martin": ["aston-martin", "aston martin", "aston", "astin martin"],
    "audi": ["audi", "audio"],
    "bentley": ["bentley", "bently", "bentely", "bentle", "bentlee"],
    "buick": ["buick", "buiick", "biuck"],
    "cadillac": ["cadillac", "caddilac", "caddillac", "cadilac", "cadillax", "caddy"],
    "ford": ["ford", "frd", "fprd", "f0rd", "frod", "fort"],
    "chevrolet": [
        "chevrolet",
        "chevy",
        "chev",
        "che y",
        "cbevrolet",
        "chverolet",
        "chverrolet",
        "cheverolet",
        "chevorlet",
        "cheverlet",
        "chevrolette",
        "cheverolette",
    ],
    "toyota": ["toyota", "toyta", "toyato", "toyoata", "toyotta", "toyoda", "toyita", "toy"],
    "honda": ["honda", "hunda", "hond", "hon da"],
    "nissan": ["nissan", "nissian", "nisan", "nisaan", "nisssan"],
    "jeep": ["jeep", "jeap", "jep", "jeepp"],
    "ram": ["ram", "ramm"],
    "gmc": ["gmc", "g m c", "g.m.c.", "general motors"],
    "bmw": ["bmw", "b m w", "beemer", "bemer", "bmm", "bwm", "bow", "mmw"],
    "chrysler": ["chrysler", "chysler", "chrystler", "crysler", "chryslar"],
    "daimler": ["daimler", "diamler", "damler", "daimlar"],
    "dodge": ["dodge", "doge", "dodg", "dodoge"],
    "eagle": ["eagle", "eagl"],
    "fiat": ["fiat", "fiaat"],
    "ferrari": ["ferrari", "ferari", "ferrrari"],
    "fisker": ["fisker", "fiskar", "fister"],
    "freightliner": ["freightliner", "freight liner", "frightliner", "freighliner", "frht"],
    "gem": ["gem", "g e m", "global electric motorcars"],
    "scion": ["scion", "sion", "scionn", "syon"],
    "suzuki": ["suzuki", "suziki", "suzuky", "sizuki", "suzucki"],
    "plymouth": ["plymouth", "plymoth", "plymout", "plymuth"],
    "genesis": ["genesis", "genisis", "genesys", "genessis"],
    "hummer": ["hummer", "humer", "hummmer"],
    "isuzu": ["isuzu", "izuzu", "iszu", "isusu", "issuzu"],
    "infiniti": ["infiniti", "infinity", "infinitti", "infineti", "infinit", "infinti", "infintiti", "infinty", "inifiniti"],
    "jaguar": ["jaguar", "jag", "jagwar", "jagaur", "jacquar"],
    "kia": ["kia", "kIA"],
    "land rover": ["land rover", "landrover", "land rove", "rover"],
    "lincoln": ["lincoln", "lincon", "linclon", "linc"],
    "lotus": ["lotus", "lotis", "louts"],
    "maserati": ["maserati", "maseratti", "masarati", "mazzerati", "maseradi"],
    "maybach": ["maybach", "mayback", "mybach"],
    "mercury": ["mercury", "mercurry", "murcury"],
    "mini": ["mini", "mini cooper", "minicooper"],
    "mitsubishi": ["mitsubishi", "mitsubish", "mitsubushi", "mitshubishi", "misubishi", "mitubushi"],
    "morgan": ["morgan"],
    "pontiac": ["pontiac", "pontac", "ponitac", "pontaic", "poniac", "pontic", "potiac"],
    "porsche": ["porsche", "porche", "porshe"],
    "rover": ["rover", "land rover", "landrover"],
    "rolls-royce": ["rolls-royce", "rolls royce", "rolls", "rols royce", "rollsroyce"],
    "saturn": ["saturn", "satern", "saturnn"],
    "smart": ["smart", "smartcar", "smart car", "smrt"],
    "subaru": ["subaru", "suburu", "subara", "subura"],
    "tesla": ["tesla", "tesala"],
    "volkswagen": [
        "volkswagen",
        "volkswagon",
        "volkswagan",
        "volkswaggen",
        "volkwagen",
        "volks",
        "vw",
        "v w",
    ],
    "volvo": ["volvo", "volvlo", "volo"],
    "lexus": ["lexus", "luxus", "lexas", "lexis", "lexuz", "lesus"],
    "mazda": ["mazda", "mazd", "masda", "madza", "mazada", "mazdda"],
    "saab": ["saab", "sab", "saabb"],
    "geo": ["geo", "g e o", "geoo"],
    "hyundai": ["hyundai", "hyndai", "hundai", "hundyai", "hyundi", "huyndai", "huiday"],
    "oldsmobile": [
        "oldsmobile",
        "olds",
        "oldsmobil",
        "oldmobile",
        "oldsmoblie",
        "oldsmobilee",
    ],
    "mercedes-benz": [
        "mercedes-benz",
        "mercedes benz",
        "mercedesbenz",
        "mercedes",
        "mecedes",
        "meercedes",
        "merceds",
        "meredes",
        "mercedez",
        "mercedez-benz",
        "benz",
        "mb",
        "mbz",
    ],
    "lamborghini": [
        "lamborghini",
        "lamborgini",
        "lambourghini",
        "lamborghinii",
        "lamborgihni",
        "lambo",
    ],
}


for aliases in MANUFACTURER_ALIASES.values():
    for alias in list(aliases):
        aliases.extend([alias.title(), alias.upper()])


MANUFACTURER_PATTERNS = [
    (manufacturer, _alias_pattern(alias))
    for manufacturer, aliases in MANUFACTURER_ALIASES.items()
    for alias in aliases
]

COMPACT_MANUFACTURER_ALIASES = [
    (manufacturer, re.sub(r"[^a-z0-9]+", "", alias.lower()))
    for manufacturer, aliases in MANUFACTURER_ALIASES.items()
    for alias in aliases
]


def discover_manufacturer_from_model(manufacturer, model):
    normalized_manufacturer = _normalize_manufacturer(manufacturer)
    s, _ = _clean_value(model)

    if s is not None:
        if normalized_manufacturer is None and re.search(r"\b(2013\s+)?genesis\s+coupe\b|\bgenesis\s+(4\s*6|5\s*0)", s):
            return "hyundai"
        if normalized_manufacturer is None and re.search(r"\bcl\s*500\b|\bcl500\b|\bsl\s*500\b|\bsl500\b|\bsl\s*class\b|merc3des\s+sl500", s):
            return "mercedes-benz"
        if normalized_manufacturer is None and re.search(r"\b850\s+sedan\b", s):
            return "volvo"
        if normalized_manufacturer is None and re.search(r"\bx\s*type\b|\bxj\s*8\b|\bxj8\b", s):
            return "jaguar"
        if normalized_manufacturer is None and re.search(r"\bimpreza\b|\bimpeza\b|\bimprezza\b|\binpreza\b", s):
            return "subaru"
        if re.search(r"chrysler|chrylser|chysler|chrystler|crysler|chryslar", s):
            return "chrysler"
        if normalized_manufacturer == "toyota" and re.search(r"\bscion\b", s):
            return "scion"
        if normalized_manufacturer == "hyundai" and re.search(r"\bg\s*(70|80|90)\b|\bg(70|80|90)\b", s):
            return "genesis"
        if re.search(r"freight\s*liner|frightliner|freighliner", s):
            return "freightliner"
        if normalized_manufacturer is None and re.search(r"\be\s*(320|350|500)\b|\be(320|350|500)\b", s):
            return "mercedes-benz"

    if normalized_manufacturer in MODEL_NORMALIZERS:
        return normalized_manufacturer

    if s is None:
        return "unknown"

    for manufacturer, pattern in MANUFACTURER_PATTERNS:
        if re.search(pattern, s):
            return manufacturer

    compact_model = re.sub(r"[^a-z0-9]+", "", s)
    for manufacturer, compact_alias in COMPACT_MANUFACTURER_ALIASES:
        if compact_alias and compact_alias in compact_model:
            return manufacturer

    alias_manufacturer, _ = _match_model_alias(s)
    if alias_manufacturer is not None:
        return alias_manufacturer

    return "unknown"


def _normalize_manufacturer(value):
    s, original = _clean_value(value)
    if s is None:
        return None

    for manufacturer, pattern in MANUFACTURER_PATTERNS:
        if re.fullmatch(pattern, s):
            return manufacturer

    return s


def normalize_model(manufacturer, model):
    normalized_manufacturer = _normalize_manufacturer(manufacturer)
    if normalized_manufacturer is None:
        _, original = _clean_value(model)
        return _unknown(original)

    normalizer = MODEL_NORMALIZERS.get(normalized_manufacturer)
    if normalizer is None:
        return _unknown(None)

    normalized_model = normalizer(model)
    if normalized_model != "unknown":
        return normalized_model

    _, alias_model = _match_model_alias(model, normalized_manufacturer)
    return alias_model or normalized_model

