# contract_data.py
"""Data handling and validation for contract generation."""

import os
import re
from datetime import datetime
import pandas as pd
from dataclasses import dataclass


@dataclass
class ContractData:
    """Data structure for contract information."""
    date: str
    gmina: str
    name: str
    postal_code: str
    city: str
    location: str
    house_number: str
    street: str = "-"
    email: str = "-"
    phone: str = "-"

    @property
    def full_address(self) -> str:
        """Combined street and house number."""
        return f"{self.street} {self.house_number}"

    def to_dict(self, contract_number: int, year: str) -> dict:
        """Convert to dictionary format for template rendering."""
        return {
            'data': self.date,
            'gmina': self.gmina,
            'nazwa': self.name,
            'kod_pocztowy': self.postal_code,
            'miasto': self.city,
            'miejscowosc': self.location,
            'ulica': self.street,
            'numer_domu': self.house_number,
            'email': self.email or "-",
            'tel': self.phone or "-",
            'nr': str(contract_number),
            'rok': year
        }


class ContractManager:
    """Handles contract data processing and storage."""

    @staticmethod
    def get_next_contract_number(output_folder: str, gmina: str, year: str) -> int:
        """Get the next available contract number."""
        if not os.path.exists(output_folder):
            return 1

        pattern = rf"Umowa_(\d+)_{year}_{gmina}_"  # Dodane 'r' przed stringiem
        max_nr = max(
            (int(match.group(1))
             for file in os.listdir(output_folder)
             if (match := re.match(pattern, file))),
            default=0
        )
        return max_nr + 1

    @staticmethod
    def save_to_excel(contract_data: dict, excel_path: str):
        """Save contract data to Excel file."""
        try:
            df = pd.DataFrame([{
                'Data umowy': contract_data['data'],
                'Numer umowy': f"{contract_data['nr']}/{contract_data['rok']}/{contract_data['gmina']}",
                'Gmina': contract_data['gmina'],
                'Nazwa/Imię i nazwisko': contract_data['nazwa'],
                'Kod pocztowy': contract_data['kod_pocztowy'],
                'Miasto': contract_data['miasto'],
                'Miejscowość': contract_data['miejscowosc'],  # Dodajemy to pole
                'Ulica': contract_data['ulica'],
                'Numer domu': contract_data['numer_domu'],
                'Email': contract_data['email'],
                'Telefon': contract_data['tel'],
                'Data dodania': datetime.now().strftime("%d.%m.%Y %H:%M")
            }])

            if os.path.exists(excel_path):
                existing_df = pd.read_excel(excel_path)
                df = pd.concat([existing_df, df], ignore_index=True)

            df.to_excel(excel_path, index=False)
        except Exception as e:
            raise ValueError(f"Nie można zapisać do pliku Excel: {str(e)}")
