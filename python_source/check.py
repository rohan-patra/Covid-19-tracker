import json
import sys

import requests
from bs4 import BeautifulSoup

output = {}
COUNTRY = {'luxembourg': 'LU', 'malawi': 'MW', 'qatar': 'QA', 'san-marino': 'SM', 'uruguay': 'UY', 'belarus': 'BY',
           'israel': 'IL', 'réunion': 'RE', 'ecuador': 'EC', 'indonesia': 'ID', 'japan': 'JP', 'tunisia': 'TN',
           'bolivia': 'BO', 'christmas-island': 'CX', 'british-virgin-islands': 'VG', 'china': 'CN',
           'isle-of-man': 'IM', 'grenada': 'GD', 'liechtenstein': 'LI', 'vanuatu': 'VU', 'vietnam': 'VN',
           'suriname': 'SR', 'djibouti': 'DJ', 'niger': 'NE', 'solomon-islands': 'SB', 'angola': 'AO', 'brunei': 'BN',
           'falkland-islands-malvinas': 'FK', 'hong-kong-sar-china': 'HK', 'guernsey': 'GG',
           'heard-and-mcdonald-islands': 'HM', 'nicaragua': 'NI', 'south-sudan': 'SS', 'pakistan': 'PK', 'yemen': 'YE',
           'australia': 'AU', 'greece': 'GR', 'jersey': 'JE', 'mayotte': 'YT', 'norway': 'NO', 'rwanda': 'RW',
           'sao-tome-and-principe': 'ST', 'american-samoa': 'AS', 'austria': 'AT', 'italy': 'IT',
           'norfolk-island': 'NF', 'papua-new-guinea': 'PG', 'aruba': 'AW', 'anguilla': 'AI', 'canada': 'CA',
           'france': 'FR', 'haiti': 'HT', 'liberia': 'LR', 'honduras': 'HN', 'kuwait': 'KW', 'mauritius': 'MU',
           'india': 'IN', 'seychelles': 'SC', 'bahrain': 'BH', 'burundi': 'BI', 'serbia': 'RS', 'timor-leste': 'TL',
           'croatia': 'HR', 'cuba': 'CU', 'togo': 'TG', 'denmark': 'DK', 'senegal': 'SN', 'albania': 'AL',
           'czech-republic': 'CZ', 'guyana': 'GY', 'kazakhstan': 'KZ', 'costa-rica': 'CR', 'nauru': 'NR',
           'new-zealand': 'NZ', 'peru': 'PE', 'saint-martin-french-part': 'MF', 'zimbabwe': 'ZW',
           'antigua-and-barbuda': 'AG', 'somalia': 'SO', 'sweden': 'SE', 'thailand': 'TH', 'saudi-arabia': 'SA',
           'central-african-republic': 'CF', 'micronesia': 'FM', 'mozambique': 'MZ', 'puerto-rico': 'PR',
           'sri-lanka': 'LK', 'south-georgia-and-the-south-sandwich-islands': 'GS', 'united-kingdom': 'GB',
           'equatorial-guinea': 'GQ', 'montenegro': 'ME', 'bosnia-and-herzegovina': 'BA', 'brazil': 'BR',
           'cocos-keeling-islands': 'CC', 'tuvalu': 'TV', 'zambia': 'ZM', 'ala-aland-islands': 'AX', 'cameroon': 'CM',
           'iceland': 'IS', 'niue': 'NU', 'chad': 'TD', 'ghana': 'GH', 'virgin-islands': 'VI',
           'turks-and-caicos-islands': 'TC', 'botswana': 'BW', 'chile': 'CL', 'latvia': 'LV', 'malta': 'MT',
           'portugal': 'PT', 'svalbard-and-jan-mayen-islands': 'SJ', 'british-indian-ocean-territory': 'IO',
           'namibia': 'NA', 'palestine': 'PS', 'samoa': 'WS', 'swaziland': 'SZ', 'us-minor-outlying-islands': 'UM',
           'iraq': 'IQ', 'macedonia': 'MK', 'sierra-leone': 'SL', 'trinidad-and-tobago': 'TT', 'eritrea': 'ER',
           'kiribati': 'KI', 'mexico': 'MX', 'nepal': 'NP', 'cape-verde': 'CV', 'colombia': 'CO', 'el-salvador': 'SV',
           'faroe-islands': 'FO', 'libya': 'LY', 'uganda': 'UG', 'mongolia': 'MN', 'belgium': 'BE',
           'congo-brazzaville': 'CG', 'germany': 'DE', 'saint-kitts-and-nevis': 'KN', 'antarctica': 'AQ',
           'guinea': 'GN', 'paraguay': 'PY', 'romania': 'RO', 'kosovo': 'XK', 'syria': 'SY', 'jordan': 'JO',
           'korea-south': 'KR', 'argentina': 'AR', 'bulgaria': 'BG', 'french-southern-territories': 'TF',
           'gambia': 'GM', 'gibraltar': 'GI', 'hungary': 'HU', 'morocco': 'MA', 'slovakia': 'SK', 'cambodia': 'KH',
           'guadeloupe': 'GP', 'oman': 'OM', 'south-africa': 'ZA', 'sudan': 'SD', 'kyrgyzstan': 'KG',
           'saint-pierre-and-miquelon': 'PM', 'slovenia': 'SI', 'venezuela': 'VE', 'azerbaijan': 'AZ', 'ireland': 'IE',
           'monaco': 'MC', 'macao-sar-china': 'MO', 'martinique': 'MQ', 'palau': 'PW', 'panama': 'PA', 'nigeria': 'NG',
           'lao-pdr': 'LA', 'marshall-islands': 'MH', 'united-arab-emirates': 'AE', 'cyprus': 'CY',
           'french-polynesia': 'PF', 'maldives': 'MV', 'mali': 'ML', 'ethiopia': 'ET', 'northern-mariana-islands': 'MP',
           'russia': 'RU', 'taiwan': 'TW', 'bangladesh': 'BD', 'guam': 'GU', 'kenya': 'KE', 'malaysia': 'MY',
           'mauritania': 'MR', 'myanmar': 'MM', 'afghanistan': 'AF', 'holy-see-vatican-city-state': 'VA',
           'netherlands': 'NL', 'saint-lucia': 'LC', 'switzerland': 'CH', 'western-sahara': 'EH', 'andorra': 'AD',
           'belize': 'BZ', 'new-caledonia': 'NC', 'madagascar': 'MG', 'pitcairn': 'PN', 'spain': 'ES', 'tonga': 'TO',
           'french-guiana': 'GF', 'jamaica': 'JM', 'bouvet-island': 'BV', 'greenland': 'GL', 'lesotho': 'LS',
           'netherlands-antilles': 'AN', 'poland': 'PL', 'united-states': 'US', 'congo-kinshasa': 'CD',
           'philippines': 'PH', 'saint-vincent-and-the-grenadines': 'VC', 'bahamas': 'BS', 'bermuda': 'BM',
           'bhutan': 'BT', 'iran': 'IR', 'singapore': 'SG', 'cayman-islands': 'KY', 'dominican-republic': 'DO',
           'egypt': 'EG', 'estonia': 'EE', 'finland': 'FI', 'montserrat': 'MS', 'comoros': 'KM', 'dominica': 'DM',
           'wallis-and-futuna-islands': 'WF', 'georgia': 'GE', 'saint-barthÃ©lemy': 'BL', 'guatemala': 'GT',
           'turkey': 'TR', 'turkmenistan': 'TM', 'benin': 'BJ', 'cote-divoire': 'CI', 'fiji': 'FJ',
           'guinea-bissau': 'GW', 'lithuania': 'LT', 'barbados': 'BB', 'gabon': 'GA', 'tajikistan': 'TJ',
           'tanzania': 'TZ', 'uzbekistan': 'UZ', 'ukraine': 'UA', 'burkina-faso': 'BF', 'cook-islands': 'CK',
           'korea-north': 'KP', 'lebanon': 'LB', 'tokelau': 'TK', 'algeria': 'DZ', 'armenia': 'AM', 'moldova': 'MD',
           'saint-helena': 'SH'}
ISO = {'LU': 'luxembourg', 'MW': 'malawi', 'QA': 'qatar', 'SM': 'san-marino', 'UY': 'uruguay', 'BY': 'belarus',
       'IL': 'israel', 'RE': 'réunion', 'EC': 'ecuador', 'ID': 'indonesia', 'JP': 'japan', 'TN': 'tunisia',
       'BO': 'bolivia', 'CX': 'christmas-island', 'VG': 'british-virgin-islands', 'CN': 'china', 'IM': 'isle-of-man',
       'GD': 'grenada', 'LI': 'liechtenstein', 'VU': 'vanuatu', 'VN': 'vietnam', 'SR': 'suriname', 'DJ': 'djibouti',
       'NE': 'niger', 'SB': 'solomon-islands', 'AO': 'angola', 'BN': 'brunei', 'FK': 'falkland-islands-malvinas',
       'HK': 'hong-kong-sar-china', 'GG': 'guernsey', 'HM': 'heard-and-mcdonald-islands', 'NI': 'nicaragua',
       'SS': 'south-sudan', 'PK': 'pakistan', 'YE': 'yemen', 'AU': 'australia', 'GR': 'greece', 'JE': 'jersey',
       'YT': 'mayotte', 'NO': 'norway', 'RW': 'rwanda', 'ST': 'sao-tome-and-principe', 'AS': 'american-samoa',
       'AT': 'austria', 'IT': 'italy', 'NF': 'norfolk-island', 'PG': 'papua-new-guinea', 'AW': 'aruba',
       'AI': 'anguilla', 'CA': 'canada', 'FR': 'france', 'HT': 'haiti', 'LR': 'liberia', 'HN': 'honduras',
       'KW': 'kuwait', 'MU': 'mauritius', 'IN': 'india', 'SC': 'seychelles', 'BH': 'bahrain', 'BI': 'burundi',
       'RS': 'serbia', 'TL': 'timor-leste', 'HR': 'croatia', 'CU': 'cuba', 'TG': 'togo', 'DK': 'denmark',
       'SN': 'senegal', 'AL': 'albania', 'CZ': 'czech-republic', 'GY': 'guyana', 'KZ': 'kazakhstan', 'CR': 'costa-rica',
       'NR': 'nauru', 'NZ': 'new-zealand', 'PE': 'peru', 'MF': 'saint-martin-french-part', 'ZW': 'zimbabwe',
       'AG': 'antigua-and-barbuda', 'SO': 'somalia', 'SE': 'sweden', 'TH': 'thailand', 'SA': 'saudi-arabia',
       'CF': 'central-african-republic', 'FM': 'micronesia', 'MZ': 'mozambique', 'PR': 'puerto-rico', 'LK': 'sri-lanka',
       'GS': 'south-georgia-and-the-south-sandwich-islands', 'GB': 'united-kingdom', 'GQ': 'equatorial-guinea',
       'ME': 'montenegro', 'BA': 'bosnia-and-herzegovina', 'BR': 'brazil', 'CC': 'cocos-keeling-islands',
       'TV': 'tuvalu', 'ZM': 'zambia', 'AX': 'ala-aland-islands', 'CM': 'cameroon', 'IS': 'iceland', 'NU': 'niue',
       'TD': 'chad', 'GH': 'ghana', 'VI': 'virgin-islands', 'TC': 'turks-and-caicos-islands', 'BW': 'botswana',
       'CL': 'chile', 'LV': 'latvia', 'MT': 'malta', 'PT': 'portugal', 'SJ': 'svalbard-and-jan-mayen-islands',
       'IO': 'british-indian-ocean-territory', 'NA': 'namibia', 'PS': 'palestine', 'WS': 'samoa', 'SZ': 'swaziland',
       'UM': 'us-minor-outlying-islands', 'IQ': 'iraq', 'MK': 'macedonia', 'SL': 'sierra-leone',
       'TT': 'trinidad-and-tobago', 'ER': 'eritrea', 'KI': 'kiribati', 'MX': 'mexico', 'NP': 'nepal',
       'CV': 'cape-verde', 'CO': 'colombia', 'SV': 'el-salvador', 'FO': 'faroe-islands', 'LY': 'libya', 'UG': 'uganda',
       'MN': 'mongolia', 'BE': 'belgium', 'CG': 'congo-brazzaville', 'DE': 'germany', 'KN': 'saint-kitts-and-nevis',
       'AQ': 'antarctica', 'GN': 'guinea', 'PY': 'paraguay', 'RO': 'romania', 'XK': 'kosovo', 'SY': 'syria',
       'JO': 'jordan', 'KR': 'korea-south', 'AR': 'argentina', 'BG': 'bulgaria', 'TF': 'french-southern-territories',
       'GM': 'gambia', 'GI': 'gibraltar', 'HU': 'hungary', 'MA': 'morocco', 'SK': 'slovakia', 'KH': 'cambodia',
       'GP': 'guadeloupe', 'OM': 'oman', 'ZA': 'south-africa', 'SD': 'sudan', 'KG': 'kyrgyzstan',
       'PM': 'saint-pierre-and-miquelon', 'SI': 'slovenia', 'VE': 'venezuela', 'AZ': 'azerbaijan', 'IE': 'ireland',
       'MC': 'monaco', 'MO': 'macao-sar-china', 'MQ': 'martinique', 'PW': 'palau', 'PA': 'panama', 'NG': 'nigeria',
       'LA': 'lao-pdr', 'MH': 'marshall-islands', 'AE': 'united-arab-emirates', 'CY': 'cyprus',
       'PF': 'french-polynesia', 'MV': 'maldives', 'ML': 'mali', 'ET': 'ethiopia', 'MP': 'northern-mariana-islands',
       'RU': 'russia', 'TW': 'taiwan', 'BD': 'bangladesh', 'GU': 'guam', 'KE': 'kenya', 'MY': 'malaysia',
       'MR': 'mauritania', 'MM': 'myanmar', 'AF': 'afghanistan', 'VA': 'holy-see-vatican-city-state',
       'NL': 'netherlands', 'LC': 'saint-lucia', 'CH': 'switzerland', 'EH': 'western-sahara', 'AD': 'andorra',
       'BZ': 'belize', 'NC': 'new-caledonia', 'MG': 'madagascar', 'PN': 'pitcairn', 'ES': 'spain', 'TO': 'tonga',
       'GF': 'french-guiana', 'JM': 'jamaica', 'BV': 'bouvet-island', 'GL': 'greenland', 'LS': 'lesotho',
       'AN': 'netherlands-antilles', 'PL': 'poland', 'US': 'united-states', 'CD': 'congo-kinshasa', 'PH': 'philippines',
       'VC': 'saint-vincent-and-the-grenadines', 'BS': 'bahamas', 'BM': 'bermuda', 'BT': 'bhutan', 'IR': 'iran',
       'SG': 'singapore', 'KY': 'cayman-islands', 'DO': 'dominican-republic', 'EG': 'egypt', 'EE': 'estonia',
       'FI': 'finland', 'MS': 'montserrat', 'KM': 'comoros', 'DM': 'dominica', 'WF': 'wallis-and-futuna-islands',
       'GE': 'georgia', 'BL': 'saint-barthÃ©lemy', 'GT': 'guatemala', 'TR': 'turkey', 'TM': 'turkmenistan',
       'BJ': 'benin', 'CI': 'cote-divoire', 'FJ': 'fiji', 'GW': 'guinea-bissau', 'LT': 'lithuania', 'BB': 'barbados',
       'GA': 'gabon', 'TJ': 'tajikistan', 'TZ': 'tanzania', 'UZ': 'uzbekistan', 'UA': 'ukraine', 'BF': 'burkina-faso',
       'CK': 'cook-islands', 'KP': 'korea-north', 'LB': 'lebanon', 'TK': 'tokelau', 'DZ': 'algeria', 'AM': 'armenia',
       'MD': 'moldova', 'SH': 'saint-helena'}
iso = str(sys.argv[1])
slug = ISO[iso]
with requests.session() as s:
    soup = BeautifulSoup(s.get(
        "https://www.google.com/search?q=population+" + iso + "&aqs=chrome..69i57j0l5j69i60l2.415j0j7&sourceid=chrome&ie=UTF-8").content,
                         'html.parser')
    element = soup.find_all(class_="BNeawe iBp4i AP7Wnd")[0]
    population = float(element.text.split()[0].replace(',', '.')) * 1000000
    soup = BeautifulSoup(s.get(
        "https://www.google.com/search?q=" + iso + "+median+age&aqs=chrome..69i57j69i64.1839j0j4&sourceid=chrome&ie=UTF-8").content,
                         'html.parser')
    element = soup.find_all(class_="BNeawe s3v9rd AP7Wnd")[0]
    median_age = element.text
    api_response = json.loads(s.get('https://api.covid19api.com/summary').text)
    for sec in api_response['Countries']:
        if sec['Slug'] == slug:
            output['Country'] = sec['Country']
            output['CountryCode'] = sec['CountryCode']
            output['NewConfirmed'] = sec['NewConfirmed']
            output['TotalConfirmed'] = sec['TotalConfirmed']
            output['NewDeaths'] = sec['NewDeaths']
            output['TotalDeaths'] = sec['TotalDeaths']
            output['NewRecovered'] = sec['NewRecovered']
            output['TotalRecovered'] = sec['TotalRecovered']
            output['TotalCasesPerMillion'] = sec['TotalConfirmed'] / population
            output['NewCasesPerMillion'] = sec['NewConfirmed'] / population
            output['TotalDeathsPerMillion'] = sec['TotalDeaths'] / population
            output['NewDeathsPerMillion'] = sec['NewDeaths'] / population
            output['CaseFatalityRatio'] = sec['TotalConfirmed'] / sec['TotalDeaths']
            output['Population'] = population
            output['MedianAge'] = median_age
            output['Date'] = sec['Date']
    print(json.dumps(output, indent=4))

