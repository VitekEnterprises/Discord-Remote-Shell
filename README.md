# Discord Remote Powershell - Educational Tool

## Important Disclaimer

**WARNING:** This is an educational demonstration tool only.  
The creators and distributors of this code accept **NO responsibility** for any damages, misuse, or legal consequences resulting from the use of this software.  
**Use at your own risk.**

**Intended Purpose:**  
This bot is designed for educational purposes to demonstrate **Discord bot development**, **PowerShell command execution**, and **system interaction concepts** in a controlled learning environment.

---

## Prerequisites

- **Python 3.8 or higher** installed on your system  
- **Discord Bot Token** from the Discord Developer Portal  
- **Administrative privileges** (required for certain PowerShell commands)  
- **Windows operating system** (PowerShell execution requires Windows)

---

## Installation Steps

### 1. Install Python Dependencies

Open **Command Prompt** or **PowerShell** as **Administrator** and run:

**text**  
pip install discord.py requests pyinstaller

---

### 2. Create a Discord Bot

Go to:  
https://discord.com/developers/applications

Click **"New Application"** and give it a name  

Navigate to the **"Bot"** section  

Click **"Add Bot"**  

Under the **"Token"** section, click **"Copy"** to copy your bot token  

Enable **"Message Content Intent"** under *Privileged Gateway Intents*

---

### 3. Configure the Bot

Open **bot.py** in a text editor  

Locate this line near the top:

**python**  
DISCORD_TOKEN = "ENTER_YOUR_DISCORD_BOT_TOKEN_HERE"

Replace **ENTER_YOUR_DISCORD_BOT_TOKEN_HERE** with your actual bot token  
(keep the quotes)

---

### 4. Invite the Bot to Your Server

In the Discord Developer Portal, go to **"OAuth2" > "URL Generator"**

Select **"bot"** under *Scopes*

Select necessary permissions  
(minimum: **"Send Messages"**, **"Read Message History"**)

Copy the generated URL and open it in your browser  

Select your server and authorize the bot

---

## Compiling to Executable (Optional)

To create a standalone executable from **bot.py**:

### Using PyInstaller

**text**  
pyinstaller --onefile --noconsole bot.py

**Command parameters:**

- **--onefile** – Creates a single executable file  
- **--noconsole** – Runs without a console window (for background operation)

---

### After Compilation

The executable will be created in the **dist/** folder  

You can rename the executable as needed  

Run the executable with **administrative privileges**

---

## Usage Instructions

### Starting the Bot

**Option 1: Run Python script directly**

**text**  
python bot.py

**Option 2: Run compiled executable**

Navigate to the **dist/** folder  

Run **bot.exe** as **Administrator**

---

## Bot Behavior

Upon startup, the bot will:

- Connect to Discord  
- Create a new text channel named with your **public IP**  
  (dots replaced with hyphens)  
- Send a confirmation message with the **current working directory**

---

## Available Commands

The bot supports the following commands in the created channel:

### Basic Commands

**Command | Description**

cd or chdir – Change directory or show current directory  
pwd – Show current working directory  
dir or ls – List directory contents  
cat, type, get-content, or gc – Display file contents  

### PowerShell Commands

Any valid **PowerShell command** can be executed directly.

---

## Security Notes

**Channel Isolation:**  
The bot creates a private channel visible only to the bot itself  

**Command Execution:**  
All commands run with the privileges of the user running the script  

**Output Handling:**  
Command output is split into chunks under **2000 characters** for Discord compatibility  

**Error Handling:**  
Errors are captured and displayed in the Discord channel

---

## Educational Context

This tool demonstrates:

- Discord bot creation and management  
- PowerShell command execution from Python  
- Subprocess management and security considerations  
- Discord API interaction  
- Error handling in multi-layer applications  
- System command execution patterns  
- Python to executable compilation with PyInstaller  

---

## Limitations and Safeguards

- **Timeout:** Commands timeout after 30 seconds  
- **Output Size:** Large outputs are truncated for Discord compatibility  
- **Channel Access:** Only the bot can access the command channel  
- **Encoding:** UTF-8 encoding is enforced for proper text handling  

---

## Legal and Ethical Considerations

By using this software, you agree that:

- You will only use this tool in environments you own or have explicit permission to test  
- You understand the potential risks of executing system commands  
- You accept full responsibility for any consequences of using this tool  
- You will comply with all applicable laws and regulations  
- This tool is for **educational purposes only**

---

## Troubleshooting

### Common Issues

**Issue | Solution**

Bot won't start – Verify Python is installed correctly. Check Discord token is valid and properly formatted. Ensure you have internet connectivity.  
Commands not executing – Run script as Administrator. Check Windows PowerShell execution policies. Verify Discord bot has proper intents enabled.  
No channel created – Bot needs **"Manage Channels"** permission. Server may have reached channel limit.  
PyInstaller compilation fails – Ensure all dependencies are installed. Run PyInstaller as Administrator. Check Python path configuration.

---

### PyInstaller Specific Issues

If compilation with PyInstaller fails:

Ensure you're using the latest version:

 
**pip install --upgrade pyinstaller**

Try with additional flags for better compatibility:


**pyinstaller --onefile --noconsole --hidden-import=discord --hidden-import=requests bot.py**

For antivirus false positives (common with PyInstaller):

- Add the executable to antivirus exclusions  
- Use a code signing certificate if available  
- Compile on the target system when possible  

---

## File Structure
  
**bot.py                    # Main Python script  **
**dist/bot.exe              # Compiled executable (after PyInstaller)  **
**build/                    # PyInstaller build directory  **

---

## Support

No official support is provided for this educational tool.  

Users are expected to have basic knowledge of:

- Python programming  
- Discord bot development  
- System administration  
- PowerShell commands  

---

## License

This tool is provided **"AS IS"** without warranty of any kind.  
Use for educational purposes only in controlled, authorized environments.

**Final Warning:**  
This tool executes system commands with the privileges of the running user.  
Use only in environments where you have explicit permission and for legitimate educational purposes.  
The creators are not responsible for any misuse or damage caused by this software.
