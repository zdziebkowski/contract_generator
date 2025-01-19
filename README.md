# Contract Generator

A dedicated application for generating waste disposal service contracts. The application enables quick contract generation with customers and maintains a contract registry in an Excel file.

## Features

- Contract generation based on a .docx template
- Automatic contract numbering
- Basic postal code validation for selected municipalities
- Contract registry in Excel format
- User-friendly interface

## Important Note on Data Validation

The application implements basic data validation focused on essential business requirements. It includes:
- Postal code validation for specific municipalities
- Required field checks
- Contract number sequence management

Full data validation (e.g., email format, phone number format) is not implemented as it wasn't required for the current business needs. Users should verify the entered data before generating contracts.

## System Requirements

- Windows 10/11
- Write permissions in the installation folder
- Microsoft Word (for opening generated contracts)
- Microsoft Excel (for viewing contract registry)

## For Users

### Installation

1. Extract `Contract_Generator.zip` to your preferred folder
2. Ensure the folder contains:
   - Contract_Generator.exe
3. Create template file for your contract in *.docx format

### First Launch

1. Run `Contract_Generator.exe`
2. Windows might display a warning about an unknown publisher on first launch
3. Click "More info" and then "Run anyway"
4. The program will automatically create required folders and files

### Usage

1. Fill in the customer data form:
   - Contract date
   - Municipality (select from list)
   - Name/Full name
   - Postal code (select from list)
   - Street
   - House number
   - Email (optional)
   - Phone (optional)

2. Click "Generate contract"
3. The generated contract will be saved in the "wystawione_umowy" folder
4. Contract data will be added to the Excel registry

## For Developers

### Development Requirements

- Python 3.11 or newer
- Poetry (dependency management)
- Git (optional, for code management)

### Development Environment Setup

1. Clone the repository:
```bash
git clone [repository-address]
cd contract-generator
```

2. Install dependencies using Poetry:
```bash
poetry install
```

### Project Structure

```
contract-generator/
├── main.py                 # Main application file
├── config.py              # Configuration (postal codes, municipalities)
├── contract_data.py       # Contract data handling
├── validators.py          # Data validation
├── gui.py                 # User interface
├── build.py              # Exe build script
├── pyproject.toml        # Poetry configuration
└── README.md             # This file
```

### Building the Application

1. Run the build script:
```bash
poetry run python build.py
```

2. The executable will be created in the `dist` folder

### Modifications

#### Adding New Municipalities

1. Open `config.py`
2. Add new municipality to `VALID_GMINAS` dictionary
3. Add postal codes for the municipality in `GMINA_POSTAL_CODES`

#### Creating and Modifying Contract Template

The contract template file is not included in the repository due to business privacy. You'll need to create your own template document. Here's how:

1. Create a new Word document named `Umowa_template.docx`
2. Design your contract using the following variables where you need dynamic content:
   - {{nr}} - contract number (automatically generated)
   - {{rok}} - year (automatically generated)
   - {{gmina}} - municipality code (selected from dropdown)
   - {{data}} - contract date (from date picker)
   - {{nazwa}} - customer name (text input)
   - {{kod_pocztowy}} - postal code (selected from dropdown)
   - {{miasto}} - city (automatically filled based on postal code)
   - {{adres}} - street and number (text input)
   - {{email}} - email (optional text input)
   - {{tel}} - phone (optional text input)

Required Document Structure:
1. The document must be in .docx format
2. Variables must be written exactly as shown above, including double curly braces
3. The template should include all your standard contract terms and conditions
4. You can include static text and formatting as needed
5. The variables will be automatically replaced with actual data when generating contracts

Example Usage in Template:
```
Contract No: {{nr}}/{{rok}}/{{gmina}}
Date: {{data}}

AGREEMENT

between [Your Company Name], hereinafter referred to as the Contractor, and

{{nazwa}}
{{adres}}
{{kod_pocztowy}} {{miasto}}
Email: {{email}}
Phone: {{tel}}

hereinafter referred to as the Client...
```

To modify existing template:
1. Open `Umowa_template.docx`
2. Edit the template while preserving the `{{variable}}` markers
3. Save the document in the same location as the executable

## Support

For application support, please contact:
- Email: wojciech.zdziebkowski@gmail.com

## License

This software is the property of Zdziebkowski Sp. z o.o. and is protected by copyright law. All rights reserved.