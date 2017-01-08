EUR_COUNTRY_CODES = ["AL", "AD", "AM", "AT", "AZ", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE", "FO", "FI", "FR", "GE", "DE", "GI", "GR", "GL", "GG", "HU", "IS", "IM", "IE", "IT", "JE", "KZ", "KG", "LV", "LI", "LT", "LU", "MK", "MT", "MD", "MC", "ME", "NL", "NO", "PL", "PT", "RO", "RU", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "TJ", "TR", "TM", "UA", "UZ"]


def classify(country_code):
    if country_code == 'GB':
        return 'GB'
    elif country_code in EUR_COUNTRY_CODES:
        return 'EUROPE'
    else:
        return 'WORLD'
