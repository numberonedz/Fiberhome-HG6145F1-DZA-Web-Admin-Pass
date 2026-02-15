# Fiberhome Password Generator WebApp

This is a PHP/MySQL web application that generates passwords for Fiberhome HG6145F1 routers based on their MAC address.

## Prerequisites

- A local web server with PHP and MySQL (e.g., [XAMPP](https://www.apachefriends.org/), [WAMP](https://www.wampserver.com/), or [MAMP](https://www.mamp.info/)).

## Installation

1.  **Move the Folder**: Copy the `fiberhome_webapp` folder to your web server's document root (e.g., `C:\xampp\htdocs\` or `C:\wamp64\www\`).
2.  **Setup Database**:
    - Open your database management tool (e.g., phpMyAdmin at `http://localhost/phpmyadmin`).
    - Create a new database named `fiberhome_db` (or just import the script below which does it for you).
    - Import the `setup_db.sql` file located in this folder.
3.  **Configure Connection**:
    - Open `db.php` and check the `$user` and `$pass` variables.
    - Default is `root` with no password. If your MySQL setup has a password, update it there.

## Usage

1.  Open your browser and navigate to `http://localhost/fiberhome_webapp/`.
2.  Enter the MAC address (format XX:XX:XX:XX:XX:XX).
3.  Click **Generate Password**.
4.  The result will appear and be saved to the history below.

## Files

- `index.php`: Main user interface.
- `api.php`: Backend logic that handles generation and database logging.
- `logic.php`: Core Python-to-PHP ported logic.
- `script.js`: Frontend interactions and AJAX calls.
- `style.css`: Glassmorphism styling.
