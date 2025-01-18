import tkinter as tk
from tkinter import ttk, messagebox
from docxtpl import DocxTemplate
import os
import re
import pandas as pd
from datetime import datetime
from tkcalendar import DateEntry

POSTAL_CODES = {
    "63-400": "Ostrów Wielkopolski",
    "63-405": "Sieroszewice",
    "63-410": "Ostrów Wielkopolski",
    "63-421": "Przygodzice",
    "63-430": "Odolanów",
    "63-435": "Sośnie",
    "63-440": "Raszków",
    "63-450": "Sobótka",
    "63-460": "Nowe Skalmierzyce"
}

VALID_GMINAS = {
    "GO": "Gmina Odolanów",
    "MO": "Miasto Odolanów",
    "O": "Odolanów",  # Changed to clarify it's Odolanów
    "R": "Raszków",
    "S": "Sieroszewice",
    "P": "Przygodzice",
    "NS": "Nowe Skalmierzyce",
    "So": "Sośnie"  # Added Sośnie
}

# Mapping between gminas and their allowed postal codes
GMINA_POSTAL_CODES = {
    "MO": ["63-400"],
    "GO": ["63-410", "63-450"],  # First one is default
    "R": ["63-440"],
    "O": ["63-430"],
    "S": ["63-405"],
    "P": ["63-421"],
    "NS": ["63-460"],
    "So": ["63-435"]
}


class ContractGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator Umów")
        self.root.geometry("600x700")

        # Store references to widgets that need updating
        self.postal_combo = None  # We'll set this in create_widgets

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_widgets(main_frame)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def create_widgets(self, frame):
        # Date selection
        ttk.Label(frame, text="Data umowy:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(frame, width=20, date_pattern='dd.mm.yyyy')
        self.date_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Gmina selection
        ttk.Label(frame, text="Gmina:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.gmina_var = tk.StringVar()
        gmina_values = [f"{code}: {name}" for code, name in VALID_GMINAS.items()]
        gmina_combo = ttk.Combobox(frame, textvariable=self.gmina_var, values=gmina_values, width=40)
        gmina_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        gmina_combo.bind('<<ComboboxSelected>>', self.update_gmina_code)

        # Name entry
        ttk.Label(frame, text="Nazwa/Imię i nazwisko:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(frame, width=40)
        self.name_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Postal code selection
        ttk.Label(frame, text="Kod pocztowy:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.postal_var = tk.StringVar()
        postal_values = [f"{code}: {city}" for code, city in POSTAL_CODES.items()]
        self.postal_combo = ttk.Combobox(frame, textvariable=self.postal_var, values=postal_values, width=40)
        self.postal_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        self.postal_combo.bind('<<ComboboxSelected>>', self.update_city)

        # City display
        ttk.Label(frame, text="Miasto:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.city_var = tk.StringVar()
        self.city_label = ttk.Label(frame, textvariable=self.city_var)
        self.city_label.grid(row=4, column=1, sticky=tk.W, pady=5)

        # Street entry (ulica)
        ttk.Label(frame, text="Ulica:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.street_entry = ttk.Entry(frame, width=40)
        self.street_entry.grid(row=5, column=1, sticky=tk.W, pady=5)

        # House number entry (numer_domu)
        ttk.Label(frame, text="Numer domu:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.house_number_entry = ttk.Entry(frame, width=40)
        self.house_number_entry.grid(row=6, column=1, sticky=tk.W, pady=5)

        # Email entry
        ttk.Label(frame, text="Email (opcjonalnie):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.grid(row=7, column=1, sticky=tk.W, pady=5)

        # Phone entry
        ttk.Label(frame, text="Telefon (opcjonalnie):").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(frame, width=40)
        self.phone_entry.grid(row=8, column=1, sticky=tk.W, pady=5)

        # Generate button
        generate_btn = ttk.Button(frame, text="Generuj umowę", command=self.generate_contract)
        generate_btn.grid(row=9, column=0, columnspan=2, pady=20)

        # Status messages
        self.status_var = tk.StringVar()
        status_label = ttk.Label(frame, textvariable=self.status_var, wraplength=500)
        status_label.grid(row=10, column=0, columnspan=2, pady=5)

        # Add Exit button next to Generate button
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)

        generate_btn = ttk.Button(button_frame, text="Generuj umowę", command=self.generate_contract)
        generate_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = ttk.Button(button_frame, text="Wyjście", command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=10)

    def clear_fields(self):
        """Clear all input fields"""
        self.date_entry.set_date(datetime.now())  # Reset to current date
        self.gmina_var.set('')
        self.name_entry.delete(0, tk.END)
        self.postal_var.set('')
        self.city_var.set('')
        self.street_entry.delete(0, tk.END)
        self.house_number_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def update_city(self, event=None):
        selected = self.postal_var.get()
        if ':' in selected:
            postal_code = selected.split(':')[0].strip()
            self.postal_var.set(postal_code)
            self.city_var.set(POSTAL_CODES.get(postal_code, ""))

    def update_gmina_code(self, event=None):
        selected = self.gmina_var.get()
        if ':' in selected:
            gmina_code = selected.split(':')[0].strip()
            self.gmina_var.set(gmina_code)

            # Update postal code based on gmina
            allowed_codes = GMINA_POSTAL_CODES.get(gmina_code, [])
            if allowed_codes:
                # Set default postal code (first in the list)
                default_code = allowed_codes[0]
                self.postal_var.set(default_code)
                self.city_var.set(POSTAL_CODES[default_code])

                # Update postal code dropdown to show only allowed values
                postal_values = [f"{code}: {POSTAL_CODES[code]}"
                                 for code in allowed_codes]
                self.postal_combo['values'] = postal_values

    def validate_inputs(self):
        if not all([
            self.date_entry.get(),
            self.gmina_var.get(),
            self.name_entry.get(),
            self.postal_var.get(),
            self.street_entry.get(),
            self.house_number_entry.get()
        ]):
            messagebox.showerror("Błąd", "Wszystkie pola (oprócz email i telefonu) są wymagane!")
            return False

        # Validate postal code for selected gmina
        gmina_code = self.gmina_var.get().split(':')[0].strip()
        postal_code = self.postal_var.get().split(':')[0].strip()

        allowed_codes = GMINA_POSTAL_CODES.get(gmina_code, [])
        if postal_code not in allowed_codes:
            messagebox.showerror(
                "Błąd",
                f"Nieprawidłowy kod pocztowy dla gminy {gmina_code}!\n"
                f"Dozwolone kody: {', '.join(allowed_codes)}"
            )
            return False

        return True

    def save_to_excel(self, contract_data, excel_path="spis_umow_automat.xlsx"):
        new_row = {
            'Data umowy': contract_data['data'],
            'Numer umowy': f"{contract_data['nr']}/{contract_data['rok']}/{contract_data['gmina']}",
            'Gmina': contract_data['gmina'],
            'Nazwa/Imię i nazwisko': contract_data['nazwa'],
            'Kod pocztowy': contract_data['kod_pocztowy'],
            'Miasto': contract_data['miasto'],
            'Ulica': contract_data['ulica'],
            'Numer domu': contract_data['numer_domu'],
            'Email': contract_data['email'],
            'Telefon': contract_data['tel'],
            'Data dodania': datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        try:
            df = pd.read_excel(excel_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=new_row.keys())

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_path, index=False)

    def get_next_contract_number(self, output_folder, gmina, rok):
        if not os.path.exists(output_folder):
            return 1

        files = os.listdir(output_folder)
        max_nr = 0
        pattern = f"Umowa_(\d+)_{rok}_{gmina}_"

        for file in files:
            match = re.match(pattern, file)
            if match:
                nr = int(match.group(1))
                max_nr = max(max_nr, nr)

        return max_nr + 1

    def generate_contract(self):
        if not self.validate_inputs():
            return

        # Prepare contract data
        data = self.date_entry.get()
        rok = data.split('.')[-1]
        gmina = self.gmina_var.get().split(':')[0].strip()
        nr = self.get_next_contract_number("wystawione_umowy", gmina, rok)

        # Combine street and house number for the template
        full_address = f"{self.street_entry.get()} {self.house_number_entry.get()}"

        contract_data = {
            'data': data,
            'gmina': gmina,
            'nazwa': self.name_entry.get(),
            'kod_pocztowy': self.postal_var.get().split(':')[0].strip(),
            'miasto': self.city_var.get(),
            'adres': full_address,  # Combined address for the template
            'ulica': self.street_entry.get(),  # Separate fields for Excel
            'numer_domu': self.house_number_entry.get(),  # Separate fields for Excel
            'email': self.email_entry.get() or "-",
            'tel': self.phone_entry.get() or "-",
            'nr': str(nr),
            'rok': rok
        }

        try:
            output_folder = "wystawione_umowy"
            os.makedirs(output_folder, exist_ok=True)

            doc = DocxTemplate("Umowa_template.docx")
            doc.render(contract_data)

            filename = f"Umowa_{contract_data['nr']}_{contract_data['rok']}_{contract_data['gmina']}_{contract_data['nazwa']}.docx"
            output_path = os.path.join(output_folder, filename)
            doc.save(output_path)

            self.save_to_excel(contract_data)

            # Update status without showing popup
            self.status_var.set(f"Umowa została wygenerowana: {output_path}")

            # Clear all fields after successful generation
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas generowania umowy: {str(e)}")
            self.status_var.set("Błąd podczas generowania umowy!")


def main():
    root = tk.Tk()
    app = ContractGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
