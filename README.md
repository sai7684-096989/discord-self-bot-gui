# Discord Self-Bot GUI

A graphical user interface (GUI) application for a Discord self-bot, built with Python and CustomTkinter. This tool provides features like nuking, raiding, spamming, and utility actions for Discord servers, with a premium version offering advanced functionalities like server cloning.

⚠️ **Important Disclaimer**: This tool is for **educational purposes only**. Using self-bots on Discord violates Discord's [Terms of Service](https://discord.com/terms) and can result in account termination. Use at your own risk. The creator of this tool is not responsible for any consequences resulting from its use.

## Features

- **Nuking**: Delete channels, roles, and ban members.
- **Raiding**: Mass DM, spam invites, and create channels/roles.
- **Spamming**: Multi-channel spam, webhook spam, and invite spam (premium).
- **Premium Features**:
  - Kick all members, delete emojis, change guild name, mass nickname changes.
  - Voice channel chaos, bypass bot security, and premium server cloning (10x faster).
- **Utility**: Mass delete messages, fetch server/user info, assign roles, lock/unlock channels.

## Prerequisites

To run this application, you need to have Python and the required dependencies installed on your system.

- **Operating System**: Windows 10 or later (other OSes may work but are untested). Chromebook Will Work So As Other Linux Distributions
- **Python**: Version 3.10 or later.
- **Dependencies**:
  - `customtkinter`: For the GUI.
  - `discord.py`: For Discord API interactions.
  - Other dependencies may be required depending on the functionality in `bot.py`, `actions.py`, `premium.py`, and `utility.py`.
- **Internet Connection**: Required for Discord API interactions.

## Installation

Follow these steps to set up and run the application on your system.

### 1. Download the Source Files
- Download the project files from the GitHub repository: [https://github.com/sai7684-096989/discord-self-bot-gui](https://github.com/sai7684-096989/discord-self-bot-gui).
- Click the green **Code** button and select **Download ZIP**.
- Extract the `.zip` file to a folder on your computer (e.g., `C:\Users\YourName\discord-self-bot-gui`).

### 2. Install Python
- If you don’t have Python installed, download and install it from [python.org](https://www.python.org/downloads/).
- During installation, make sure to check the box to **“Add Python to PATH”**.
- Verify Python is installed by opening a Command Prompt (Windows) or terminal (Mac/Linux) and running:
  ```cmd
  python --version
  ```
  ### Install Dependencies

  - Open Up command prompt Or terminal and run
``` python3 -m venv .venv```
- afterwards run the following
```source .venv/bin/activate```
```pip install discord.py```
```pip install customtkinter```
```pip install discord.py-self customtkinter aiohttp ```
- Now Run
  ```cd Python```
  ```python main.py```
- And Enjoy!
