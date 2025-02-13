# gui.py
"""GUI components for the Contract Generator."""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from typing import Callable, Any, Dict
from config import POSTAL_CODES, VALID_GMINAS, GMINA_POSTAL_CODES


class PathSettings(ttk.LabelFrame):
    """Frame for path configuration settings."""

    def __init__(self, parent, path_vars: Dict[str, tk.StringVar], callbacks: Dict[str, Callable]):
        super().__init__(parent, text="Ustawienia ścieżek", padding="5")
        self.path_vars = path_vars
        self.callbacks = callbacks
        self._create_widgets()

    def _create_widgets(self):
        """Create path setting widgets."""
        paths = [
            ("Plik szablonu:", "template"),
            ("Folder umów:", "contracts"),
            ("Folder dla pliku Excel:", "excel")
        ]

        for row, (label_text, var_name) in enumerate(paths):
            ttk.Label(self, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=2)
            ttk.Entry(self, textvariable=self.path_vars[var_name], width=50).grid(
                row=row, column=1, pady=2, padx=5)
            ttk.Button(
                self,
                text="Wybierz",
                command=self.callbacks[f"select_{var_name}"]
            ).grid(row=row, column=2, pady=2)


class ContractForm(ttk.Frame):
    """Main contract form interface."""

    def __init__(self, parent, data_vars: Dict[str, tk.StringVar], callbacks: Dict[str, Callable]):
        super().__init__(parent)
        self.data_vars = data_vars
        self.callbacks = callbacks
        self._create_widgets()

    def _create_widgets(self):
        """Create form widgets."""
        # Data field
        self.date_entry = self._add_field("Data umowy:", DateEntry,
                                          {"width": 20, "date_pattern": "dd.mm.yyyy"})

        # Gmina field
        gmina_values = [f"{code}: {name}" for code, name in VALID_GMINAS.items()]
        self.gmina_combo = self._add_field("Gmina:", ttk.Combobox,
                                           {"values": gmina_values, "width": 40,
                                            "textvariable": self.data_vars["gmina"]})
        self.gmina_combo.bind('<<ComboboxSelected>>', lambda e: self.callbacks["on_gmina_select"]())

        # Name field
        self.name_entry = self._add_field("Nazwa/Imię i nazwisko:", ttk.Entry,
                                          {"width": 40})

        # Postal code field
        postal_values = [f"{code}: {city}" for code, city in POSTAL_CODES.items()]
        self.postal_combo = self._add_field("Kod pocztowy:", ttk.Combobox,
                                            {"values": postal_values, "width": 40,
                                             "textvariable": self.data_vars["postal"]})
        self.postal_combo.bind('<<ComboboxSelected>>', lambda e: self.callbacks["on_postal_select"]())

        # City display
        self.city_label = self._add_field("Miasto:", ttk.Label,
                                          {"textvariable": self.data_vars["city"]})

        # Location field
        self.location_entry = self._add_field("Miejscowość:", ttk.Entry,
                                              {"width": 40})

        # Street field
        self.street_entry = self._add_field("Ulica:", ttk.Entry,
                                            {"width": 40})

        # House number field
        self.house_entry = self._add_field("Numer domu:", ttk.Entry,
                                           {"width": 40})

        # Optional fields
        self.email_entry = self._add_field("Email (opcjonalnie):", ttk.Entry,
                                           {"width": 40})
        self.phone_entry = self._add_field("Telefon (opcjonalnie):", ttk.Entry,
                                           {"width": 40})

        ttk.Label(self, text="").grid(row=11, column=0, pady=10)  # Dodatkowy odstęp

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=12, column=0, columnspan=2, pady=20)  # Zwiększone pady z 10 na 20

        ttk.Button(button_frame, text="Generuj umowę",
                   command=self.callbacks["generate"]).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Wyjście",
                   command=self.callbacks["exit"]).pack(side=tk.LEFT, padx=10)

        # Status message
        status_label = ttk.Label(self, textvariable=self.data_vars["status"],
                                 wraplength=500)
        status_label.grid(row=13, column=0, columnspan=2, pady=5)

    def _add_field(self, label: str, widget_class: Any, widget_kwargs: dict = None) -> Any:
        """Helper method to add form fields."""
        widget_kwargs = widget_kwargs or {}
        row = len(self.grid_slaves()) // 2

        ttk.Label(self, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
        widget = widget_class(self, **widget_kwargs)
        widget.grid(row=row, column=1, sticky=tk.W, pady=5)

        return widget

    def get_values(self) -> dict:
        """Get all form values."""
        return {
            "data": self.date_entry.get(),
            "gmina": self.data_vars["gmina"].get().split(':')[0].strip() if ':' in self.data_vars["gmina"].get() else
            self.data_vars["gmina"].get(),
            "nazwa": self.name_entry.get(),
            "kod_pocztowy": self.data_vars["postal"].get().split(':')[0].strip() if ':' in self.data_vars[
                "postal"].get() else self.data_vars["postal"].get(),
            "miasto": self.data_vars["city"].get(),
            "miejscowosc": self.location_entry.get(),
            "ulica": self.street_entry.get(),
            "numer_domu": self.house_entry.get(),
            "email": self.email_entry.get() or "-",
            "tel": self.phone_entry.get() or "-",
        }

    def clear_fields(self):
        """Clear all form fields."""
        entries = [self.name_entry, self.street_entry, self.house_entry,
                   self.email_entry, self.phone_entry, self.location_entry]
        for entry in entries:
            entry.delete(0, tk.END)

        self.data_vars["gmina"].set("")
        self.data_vars["postal"].set("")
        self.data_vars["city"].set("")

    def update_postal_codes(self, allowed_codes: list):
        """Update postal code combobox values based on selected gmina."""
        postal_values = [f"{code}: {POSTAL_CODES[code]}" for code in allowed_codes]
        self.postal_combo['values'] = postal_values
        if postal_values:
            self.postal_combo.set(postal_values[0])