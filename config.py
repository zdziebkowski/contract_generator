# config.py
"""Configuration settings and constants for the Contract Generator application."""

POSTAL_CODES = {
    "63-400": "Ostrów Wielkopolski",
    "63-405": "Sieroszewice",
    "63-410": "Ostrów Wielkopolski",
    "63-421": "Przygodzice",
    "63-430": "Odolanów",
    "63-440": "Raszków",
    "63-450": "Sobótka",
}

VALID_GMINAS = {
    "GO": "Gmina Ostrów",
    "MO": "Miasto Ostrów",
    "O": "Odolanów",
    "R": "Raszków",
    "S": "Sieroszewice",
    "P": "Przygodzice",
}

GMINA_POSTAL_CODES = {
    "MO": ["63-400"],
    "GO": ["63-410", "63-450", "63-400"],
    "R": ["63-440"],
    "O": ["63-430"],
    "S": ["63-405"],
    "P": ["63-421"],
}

GMINA_LOCATIONS = {
    "MO": [],
    "GO": [
        "Baby", "Bagatela", "Będzieszyn", "Biłgoraje", "Biniew", "Borowiec",
        "Borowina", "Cegły", "Chruszczyny", "Czekanów", "Daniszyn", "Fabryka",
        "Franklinów", "Gorzyce Wielkie", "Górzenko", "Górzno", "Gręblów",
        "Gutów", "Jamy", "Kamionka", "Karski", "Kawetczyzna", "Kąkolewo",
        "Kołątajew", "Kwiatków", "Lamki", "Lewkowiec", "Lewków", "Łąkociny",
        "Mazury", "Michałków", "Młynów", "Nowe Kamienice", "Onęber", "Palczew",
        "Radziwiłłów", "Rejtanów", "Sadowie", "Słaborowice",
        "Smardowskie Olendry", "Sobczyna", "Sobótka", "Stary Staw", "Szczury",
        "Świeligów", "Topola Mała", "Trąba", "Warszty", "Wtórek",
        "Wysocko Wielkie", "Zacharzew", "Zalesie"
    ],
    "O": [
        "Baby", "Bałamącek", "Biadaszki", "Boników", "Chałupki", "Garki",
        "Gliśnica", "Gorzyce Małe", "Gorzyczki", "Grochowiska", "Harych",
        "Huta", "Kaczory", "Karłowice", "Kuroch", "Lipiny", "Mogiłka",
        "Mościska", "Nabyszyce", "Nadstawki", "Papiernia", "Raczyce",
        "Szmata", "Ściegna", "Świeca", "Tarchały Małe", "Tarchały Wielkie",
        "Trzcieliny", "Uciechów", "Wierzbno", "Wisławka", "Zawidza",
        "Żuraw", "Odolanów"
    ],
    "R": [
        "Bieganin", "Bieganinek", "Bugaj", "Drogosław", "Florek", "Głogowa",
        "Grudzielec", "Grudzielec Nowy", "Janków Zaleśny", "Jaskółki",
        "Jelitów", "Józefów", "Koryta", "Korytnica", "Ligota", "Majchry",
        "Moszczanka", "Niemojewiec", "Nychy", "Pogrzybów", "Przybysławice",
        "Radłów", "Raszkówek", "Rąbczyn", "Skrzebowa", "Sulisław",
        "Szczurawice", "Walentynów", "Raszków"
    ],
    "P": [
        "Antonin", "Bażantarnia", "Bogufałów", "Chynowa", "Czarnylas",
        "Dębnica", "Hetmanów", "Janków Przygodzki", "Jezioro", "Katarzynów",
        "Klady", "Kocięba", "Krzyżaki", "Laski", "Ludwików", "Pardalin",
        "Popłomyk", "Przygodziczki", "Smardów", "Strugi", "Tarchalskie",
        "Topola Wielka", "Topola-Osiedle", "Trzcieliny", "Wysocko Małe",
        "Zawidzyn", "Przygodzice"
    ],
    "S": [
        "Bibianki", "Biernacice", "Bilczew", "Biskupice", "Fidela",
        "Górski Młyn", "Ilski Młyn", "Kaliszkowice", "Kania", "Kęszyce",
        "Kowalew", "Latowice", "Małolepsza", "Masanów", "Miłaszka", "Młynik",
        "Namysłaki", "Ołobok", "Parczew", "Piaski", "Psary", "Rachuta",
        "Raduchów", "Rososzyca", "Sieroszewice", "Sławin", "Spalony",
        "Stara Wieś", "Strzyżew", "Strzyżewek", "Urban", "Westrza",
        "Wielowieś", "Wielowieś", "Wydarta", "Wygoda", "Zamość", "Zawicki",
        "Zmyślona", "Sieroszewice"
    ]
}

MAIN_LOCATIONS = {
    "MO": "Ostrów Wielkopolski",
    "O": "Odolanów",
    "R": "Raszków",
    "P": "Przygodzice",
    "S": "Sieroszewice"
}

DEFAULT_PATHS = {
    "template": "Umowa_template.docx",
    "contracts": "wystawione_umowy",
    "excel": "wystawione_umowy",
    "excel_filename": "spis_umow_automat.xlsx"
}