# main.py
"""Main entry point for the Contract Generator application."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from docxtpl import DocxTemplate
import os
from datetime import datetime

from config import DEFAULT_PATHS, POSTAL_CODES, VALID_GMINAS, GMINA_POSTAL_CODES
from gui import PathSettings, ContractForm
from validators import ContractValidator
from contract_data import ContractData, ContractManager


class ContractGeneratorApp:
    """Main application class for Contract Generator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Generator Umów")
        self.root.geometry("800x900")

        default_font = ('TkDefaultFont', 12)  # zwiększenie z domyślnego 9/10 na 12
        self.root.option_add('*Font', default_font)

        style = ttk.Style()
        style.configure('.', font=default_font)

        # Initialize variables
        self.path_vars = self._init_path_vars()
        self.data_vars = self._init_data_vars()

        # Initialize components
        self.validator = ContractValidator()
        self.contract_manager = ContractManager()

        self._setup_main_window()

    def _init_path_vars(self):
        """Initialize path-related variables."""
        return {
            "template": tk.StringVar(value=DEFAULT_PATHS["template"]),
            "contracts": tk.StringVar(value=DEFAULT_PATHS["contracts"]),
            "excel": tk.StringVar(value=DEFAULT_PATHS["excel"])
        }

    def _init_data_vars(self):
        """Initialize data-related variables."""
        return {
            "status": tk.StringVar(),
            "gmina": tk.StringVar(),
            "postal": tk.StringVar(),
            "city": tk.StringVar()
        }

    def _setup_main_window(self):
        """Setup the main application window."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create path settings
        path_callbacks = {
            "select_template": self._select_template,
            "select_contracts": self._select_contracts_dir,
            "select_excel": self._select_excel_dir
        }
        path_settings = PathSettings(main_frame, self.path_vars, path_callbacks)
        path_settings.grid(row=0, column=0, sticky='ew')

        # Add separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=1, column=0, sticky='ew', pady=10)

        # Create contract form
        form_callbacks = {
            "on_gmina_select": self._on_gmina_select,
            "on_postal_select": self._on_postal_select,
            "generate": self._generate_contract,
            "exit": self.root.quit
        }
        self.contract_form = ContractForm(main_frame, self.data_vars, form_callbacks)
        self.contract_form.grid(row=2, column=0, sticky='nsew')

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _on_gmina_select(self):
        """Handle gmina selection."""
        selected = self.data_vars["gmina"].get()
        if ':' in selected:
            gmina_code = selected.split(':')[0].strip()
            self.data_vars["gmina"].set(gmina_code)

            allowed_codes = GMINA_POSTAL_CODES.get(gmina_code, [])
            self.contract_form.update_postal_codes(allowed_codes)

            if len(allowed_codes) == 1:
                postal_code = allowed_codes[0]
                self.data_vars["postal"].set(postal_code)
                self.data_vars["city"].set(POSTAL_CODES.get(postal_code, ""))

            self.contract_form.update_locations(gmina_code)

    def _select_template(self):
        """Handle template file selection."""
        filename = filedialog.askopenfilename(
            title="Wybierz plik szablonu",
            filetypes=[("Dokumenty Word", "*.docx"), ("Wszystkie pliki", "*.*")]
        )
        if filename:
            self.path_vars["template"].set(filename)

    def _select_contracts_dir(self):
        """Handle contracts directory selection."""
        directory = filedialog.askdirectory(title="Wybierz folder na umowy")
        if directory:
            self.path_vars["contracts"].set(directory)

    def _select_excel_dir(self):
        """Handle Excel directory selection."""
        directory = filedialog.askdirectory(title="Wybierz folder dla pliku Excel")
        if directory:
            self.path_vars["excel"].set(directory)

    def _on_postal_select(self):
        """Handle postal code selection."""
        selected = self.data_vars["postal"].get()
        if ':' in selected:
            postal_code = selected.split(':')[0].strip()
            self.data_vars["postal"].set(postal_code)
            self.data_vars["city"].set(POSTAL_CODES.get(postal_code, ""))

    def _generate_contract(self):
        """Generate the contract document."""
        try:
            # Validate paths
            self.validator.validate_paths(
                self.path_vars["template"].get(),
                [self.path_vars["contracts"].get(), self.path_vars["excel"].get()]
            )

            # Get form values
            values = self.contract_form.get_values()
            year = datetime.now().strftime("%Y")

            # Get next contract number
            contract_number = self.contract_manager.get_next_contract_number(
                self.path_vars["contracts"].get(),
                values["gmina"],
                year
            )

            # Create contract data
            contract_data = ContractData(
                date=values["data"],
                gmina=values["gmina"],
                name=values["nazwa"],
                postal_code=values["kod_pocztowy"],
                city=values["miasto"],
                location=values["miejscowosc"],
                street=values["ulica"],
                house_number=values["numer_domu"],
                email=values["email"],
                phone=values["tel"],
                is_eco=values["is_eco"],
                nip=values["nip"]
            )

            # Validate data
            self.validator.validate_required_fields(contract_data)
            self.validator.validate_postal_code(
                contract_data.gmina,
                contract_data.postal_code,
                GMINA_POSTAL_CODES
            )

            # Generate contract
            template_data = contract_data.to_dict(contract_number, year)
            doc = DocxTemplate(self.path_vars["template"].get())
            doc.render(template_data)

            # Save contract
            filename = f"Umowa_{contract_number}_{year}_{values['gmina']}_{values['nazwa']}.docx"
            output_path = os.path.join(self.path_vars["contracts"].get(), filename)
            doc.save(output_path)

            # Save to Excel
            excel_path = os.path.join(
                self.path_vars["excel"].get(),
                DEFAULT_PATHS["excel_filename"]
            )
            self.contract_manager.save_to_excel(template_data, excel_path)

            self.data_vars["status"].set(f"Umowa została wygenerowana: {filename}")
            self.contract_form.clear_fields()

        except Exception as e:
            messagebox.showerror("Błąd", str(e))
            self.data_vars["status"].set("Błąd podczas generowania umowy!")


def main():
    """Application entry point."""
    root = tk.Tk()
    app = ContractGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
