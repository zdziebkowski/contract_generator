import PyInstaller.__main__
import sys
from pathlib import Path

def build_exe():
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()

    PyInstaller.__main__.run([
        'main.py',
        '--name=Contract_Generator',
        '--onefile',
        '--windowed',
        '--add-data=Umowa_template.docx;.',
        '--icon=contract.ico',  # Add icon
        '--clean',
        '--path=.',
        # Add hidden imports for required packages
        '--hidden-import=babel.numbers',
        '--hidden-import=docxtpl',
        '--hidden-import=tkcalendar',
        '--hidden-import=openpyxl',
    ])


if __name__ == '__main__':
    build_exe()