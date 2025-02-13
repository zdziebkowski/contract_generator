# validators.py
"""Validation functions for the Contract Generator."""

from typing import List, Dict
import os
from contract_data import ContractData


class ContractValidator:
    """Validates contract data and paths."""

    @staticmethod
    def validate_paths(template_path: str, output_dirs: List[str]) -> bool:
        """Validate file paths and create directories if needed."""
        if not os.path.isfile(template_path):
            raise ValueError("Nie znaleziono pliku szablonu!")

        for directory in output_dirs:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                raise ValueError(f"Błąd podczas tworzenia katalogów: {str(e)}")
        return True

    @staticmethod
    def validate_required_fields(contract_data: ContractData) -> bool:
        """Validate required contract fields."""
        required_fields = [
            contract_data.date,
            contract_data.gmina,
            contract_data.name,
            contract_data.postal_code,
            contract_data.house_number
        ]

        if not all(required_fields):
            raise ValueError("Wszystkie pola (oprócz email i telefonu) są wymagane!")
        return True

    @staticmethod
    def validate_postal_code(gmina: str, postal_code: str, valid_codes: Dict[str, List[str]]) -> bool:
        """Validate postal code for selected gmina."""
        allowed_codes = valid_codes.get(gmina, [])
        if postal_code not in allowed_codes:
            raise ValueError(
                f"Nieprawidłowy kod pocztowy dla gminy {gmina}!\n"
                f"Dozwolone kody: {', '.join(allowed_codes)}"
            )
        return True
