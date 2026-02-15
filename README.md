# Fiberhome HG6145F1 (Algeria) Password Generator

This repository contains tools to generate the administrative password for Fiberhome HG6145F1 routers (common in Algeria) using the device's MAC address.

## Tools Included

### 1. Standalone GUI Application (`gui/`)
The easiest way to use the tool. It's a single executable file that launches a local web interface.
- **Features**: Auto-detects your router's MAC address, generates password instantly.
- **Usage**:
    1. Download `fiberhome_gui.exe` (if available in releases) or build it yourself.
    2. Run the executable. It opens your browser automatically.
    3. Click "Detect" or enter MAC manually.

### 2. PHP Web Application (`web/`)
For hosting on a web server (e.g., XAMPP, WAMP, or a live server).
- **Features**: History log (MySQL), mobile-friendly interface.
- **Setup**:
    1. Copy contents of `web/` to your web server (e.g., `htdocs`).
    2. Create a database named `fiberhome_db` and import `setup_db.sql`.
    3. Configure `db.php` if you have a database password.

### 3. CLI Script (`cli/`)
A simple Python script for command-line usage.
- **Usage**: `python fiberhome_keygen.py`

## Building from Source

To build the standalone executables on Windows:

1. Install Python 3.x.
2. Install dependencies:
   ```bash
   pip install flask pyinstaller
   ```
3. Run the build script:
   ```cmd
   cd build
   build_executables.bat
   ```
4. Find the `.exe` files in the `dist` folder.

## Credits
Based on the logic by Adel/NumberOneDz.
