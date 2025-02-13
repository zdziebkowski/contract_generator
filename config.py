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

DEFAULT_PATHS = {
    "template": "Umowa_template.docx",
    "contracts": "wystawione_umowy",
    "excel": "wystawione_umowy",
    "excel_filename": "spis_umow_automat.xlsx"
}