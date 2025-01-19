# Contract Generator

A dedicated application for generating waste disposal service contracts, developed as a solution for automating contract management processes. This project demonstrates the implementation of a business automation tool using Python and modern development practices.

## Features

### Core Functionality
- Contract generation based on customizable .docx templates
- Automatic contract numbering with municipality-specific sequences
- Postal code validation for selected municipalities
- Comprehensive contract registry in Excel format
- User-friendly graphical interface
- Automatic data validation and error checking
- Separate address fields for street and house number
- Electronic document handling

### Important Note on Data Validation
The application implements targeted data validation focusing on critical business requirements:
- Municipality-specific postal code validation
- Required field verification
- Contract number sequence management
- Address format validation
- Basic data integrity checks

Note: Advanced validation (email format, phone number format) is not implemented as per current business requirements. Users should verify data accuracy before contract generation.

### System Requirements
- Operating System: Windows 10 or Windows 11
- Required Software:
  - Microsoft Word (for contract generation and viewing)
  - Microsoft Excel (for registry access)
- System Access:
  - Write permissions in the installation directory
  - Network access for multi-user environments
- Hardware:
  - Minimum 4GB RAM
  - 100MB free disk space

### Usage Process
1. **Initial Setup**
   - Install application from provided package
   - Verify template file availability
   - Configure user permissions

2. **Customer Data Entry**
   - Select contract date
   - Choose municipality from approved list
   - Enter customer details:
     * Full name/Company name
     * Address information
     * Contact details (optional)

3. **Contract Generation**
   - System validates all entered data
   - Generates unique contract number
   - Creates contract document from template
   - Saves in designated folder structure

4. **Registry Management**
   - Automatically updates Excel registry
   - Maintains contract sequence
   - Stores customer information
   - Enables easy contract tracking

5. **Document Handling**
   - Generated contracts saved in 'wystawione_umowy'
   - Original template preserved
   - Backup system for generated documents

## Technical Implementation

### Technologies Used
- Python 3.11
- Poetry for dependency management
- PyQt6 for the graphical interface
- python-docx for Word document handling
- pandas for Excel registry management
- Custom validation system for business rules

### Architecture Highlights
The project follows a modular architecture with clear separation of concerns:
```
contract-generator/
├── main.py                 # Application entry point and initialization
├── config.py              # Configuration management
├── contract_data.py       # Contract data handling and processing
├── validators.py          # Custom validation system
├── gui.py                 # User interface implementation
└── build.py              # Build system for executable generation
```

### Key Development Features
1. **Template System**
   - Implemented dynamic document generation using python-docx
   - Created a variable replacement system for template processing
   - Developed robust error handling for document processing

2. **Data Validation**
   - Built a custom validation system for postal codes
   - Implemented business rule validation
   - Created user input validation with immediate feedback

3. **User Interface**
   - Designed an intuitive form-based interface
   - Implemented real-time validation feedback
   - Created a streamlined contract generation workflow

4. **Data Management**
   - Developed an Excel-based registry system
   - Implemented automatic contract numbering
   - Created data persistence for configuration

5. **Build System**
   - Set up automated build process using PyInstaller
   - Configured dependency management with Poetry
   - Implemented version control with Git

## Development Process

### Project Setup and Dependencies
```bash
# Environment setup using Poetry
poetry init
poetry add PyQt6 python-docx pandas
poetry add --group dev pytest pyinstaller
```

### Build Process
```bash
# Building executable
poetry run pyinstaller --onefile --windowed main.py
```

### Development Best Practices
- Modular code structure for maintainability
- Comprehensive error handling
- User-centric design approach
- Automated build process
- Version control with Git

## Installation Instructions

1. Extract `Contract_Generator.zip` to your preferred folder
2. Ensure the folder contains:
   - Contract_Generator.exe
   - Umowa_template.docx (contract template)

### First Launch

1. Run `Contract_Generator.exe`
2. Windows might display a warning about an unknown publisher on first launch
3. Click "More info" and then "Run anyway"
4. The program will automatically create required folders and files

## Contract Template Structure

The contract template uses the following variables for dynamic content:
- {{nr}} - contract number (automatically generated)
- {{rok}} - year (automatically generated)
- {{gmina}} - municipality code
- {{data}} - contract date
- {{nazwa}} - customer name
- {{kod_pocztowy}} - postal code
- {{miasto}} - city
- {{adres}} - street and number
- {{email}} - email
- {{tel}} - phone

## Support

For application support, please contact:
- Email: wojciech.zdziebkowski@gmail.com

## License and Usage

© 2024 Zdziebkowscy Sp. z o.o. All rights reserved.
The technical documentation provided here outlines the development approach and implementation details while the software itself remains under exclusive ownership of Zdziebkowscy Sp. z o.o.