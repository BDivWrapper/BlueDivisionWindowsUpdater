# Blue Division Windows Updater

This repository contains the Python script for the Blue Division Windows updater. The updater checks for updates to both the game and the script, allowing users to easily download and install updates.

## Features

- **Automatic Updates**: Checks for and installs updates for the script and the game.
- **User-Friendly Interface**: Uses popups for notifications and update prompts.

## Build the Executable Yourself

If you prefer to build the executable yourself, follow these steps:

### Prerequisites

1. **Python**: Install Python from [python.org](https://www.python.org/downloads/).
2. **Install Required Packages**: Open a terminal and run:
   ```bash
   pip install requests pyinstaller
   ```

### Steps to Build

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BDivWrapper/BlueDivisionWindowsUpdater.git
   cd BlueDivisionWindowsUpdater
   ```

2. **Build the Executable**:
   ```bash
   pyinstaller --onefile --noconsole auto_updater.py
   ```
   The executable will be in the `dist/` folder.

3. **Run the Executable**:
   Double-click the executable in `dist/auto_updater.exe` to check for updates and launch the game.

## Config File

The updater uses a `config.txt` file to track the current script and game versions. This file is created automatically.

## Contributing

Feel free to fork this repository and submit a pull request if you have improvements or fixes.
