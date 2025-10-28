#!/usr/bin/env python3
import os
import hashlib
import json
import getpass
import time
import sys
import datetime
import socket
import platform
import random

# === METADATA ===
# Termux Lock Advanced Edition
# Author: Pratham (Hackerk_17)
# License: MIT

# === PATHS ===
HOME = os.path.expanduser("~")
LOCK_DIR = os.path.join(HOME, ".termux_lock")
PASS_FILE = os.path.join(LOCK_DIR, "pass.json")
LOG_FILE = os.path.join(LOCK_DIR, "intruder.log")

# === COLORS ===
R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
W = "\033[0m"

# === BANNER (compact dragon / skull style) ===
BANNER = f"""{R}
       ...:;::lo;.'''........            ..........             ......'....'coc:;,.. .
    .,.,c;;,;;,'.....'''''...           ..  ..           ...''.''.....';;;;;,c, ...
    .:c,;ll:;,,.........;;,.ll.      .                 .cx;,;'.........',;;cl;':;..
     .;cccc:;''''''...''..:;c:l.  .;lol:,,..   .      .l;l,:..''...''''..;;c:c:;. .
      .;cccc;,',,''''.'.....';,..:xl:,ll;'..           ,;,.....,.''''',,',:ccc:.  .
        .';;;;,'.''....',.....;okl,..:xlc..,;:;,,,,..  ......''....''.',;;;;,.    .
      ....'.'''...'''...'.....occlc;'....,cccclccccll:;......'...'''....','''...  .
       ..'''....'..''''...,'. ......';:;;,'..'.'..',;:ldc;',...'''''......',,'.   .
      ',''',,,'...''..''....;c::;:;;'',;;clllc;,.....',;cl:,..''..''...',,,''.,'  .
     .','''...............'lcc,,'.';ldxxxxxxxxxxxd:'...''coc,..............''',,. .
     .,,'''.............. .''.  .:loxxxxxxddxxxxxxdlc,..',;cd,..............''',. .
      ..''''''........''..... ..ccccllloollllodllolll::..';,cc.'.....'''''''''..  .
       .'','............... .'.,::lclcllclllccclcccll;:. ,''cl.......''...',,'.   .
        .''',,'.......'....','.,,;doooc:c:cc:cclooodl,;..',;c:.........',,''..    .
         ....'.'..........:;'. ...odooddolcccoddoooo'.. ..,c:. .........''..
          .,'','''...... ,c;.   .:.....;;:'':c;'....;...',;,........'''''','.
           ...'..........c:c'   ,.      ..cl..       ; .,'.............''..
               .. .'.....,;c'.  ;:......,:'.;;'... .,c .    ......'. ...
              .  .'. ...  ',''..,lol;',:c.   cc,,;coo,'     ..... .'.  .
                 '. ....  ..... .....;c;,    .::;.  ..  .. ......  .'..
                    .  ....   ...    'col:::;lll'      ..  ... ...
                    .. .    .'....   .;;,;c;;::,. .     .,'  ..  ..
                   ..      'c'..   ..  ..,:;.,'. .'...,;,;;      .
                    .      '::.    .;..         .:...'...        .
                    ...    .';;,,''..;.. .... ..,.             ....
                             ......  .;. .... .',  .             .
                            ..   .   .;.  .. ..c.  ..    ..
                            .    ..   .:,.''',c'    .    .
                                 .'    ..'.....    ..
                                   ...     .    .''.                           
                                     ..........'..
{Y}        Made by Pratham  |  Instagram:- Hackerk_17{W}
"""

# === UTIL: password hashing ===
def hash_pass(password, salt=None):
    """
    Returns dict with 'salt' and 'hash' using PBKDF2-HMAC-SHA256.
    """
    if not salt:
        salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200000).hex()
    return {"salt": salt, "hash": hashed}

def verify_pass(password, data):
    """
    Verify given password against stored data (dict with salt and hash).
    """
    new = hash_pass(password, data["salt"])
    return new["hash"] == data["hash"]

# === STORAGE ===
def save_pass(data):
    os.makedirs(LOCK_DIR, exist_ok=True)
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_pass():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None

# === INTRUDER LOG ===
def log_intruder(username):
    """
    Append an intruder attempt line to the intruder log.
    """
    os.makedirs(LOCK_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        host = socket.gethostname()
        log.write(f"[{t}] Intruder attempt by '{username}' on {host}\n")

# === PROGRESS (unlock animation) ===
def progress(msg="Unlocking"):
    bar_length = 20
    for i in range(1, bar_length + 1):
        filled = "#" * i
        empty = "." * (bar_length - i)
        percent = int((i / bar_length) * 100)
        sys.stdout.write(f"\r{Y}{msg} [{filled}{empty}] {percent}%{W}")
        sys.stdout.flush()
        time.sleep(0.05)
    # final newline + flush to avoid stray characters on next shell prompt
    sys.stdout.write("\n")
    sys.stdout.flush()
    print(f"{G}✔ Access Granted!{W}\n")

# === FAKE PROMPT DELAY (animated progress bar variant) ===
def fake_delay_animated():
    print(f"\n{R}[!] Multiple failed attempts detected!{W}")
    print(f"{Y}System analyzing potential threats...{W}")
    # animated "analysis" bar
    for i in range(1, 41):
        filled = int((i / 40) * 30)
        bar = "#" * filled + "." * (30 - filled)
        sys.stdout.write(f"\r{C}Analyzing [{bar}] {int((i/40)*100)}%{W}")
        sys.stdout.flush()
        time.sleep(0.08)
    # ensure clean newline + flush
    sys.stdout.write("\n")
    sys.stdout.flush()
    print(f"\n{R}Deep analysis complete. Locking for 12 seconds...{W}")
    time.sleep(12)
    # clear screen after the delay
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    sys.stdout.flush()

# === WELCOME MESSAGE (single line only) ===
def welcome_message():
    # Only the single welcome message requested.
    print(f"{G}Stay anonymous, stay secure 🕶️{W}")

# === PASSWORD CHANGE ===
def change_password():
    data = load_pass()
    if not data:
        print(f"{R}No existing password found. Run the setup first.{W}")
        return
    old = getpass.getpass(f"{Y}Enter old password: {W}")
    if not verify_pass(old, data):
        print(f"{R}Incorrect old password!{W}")
        return
    new = getpass.getpass(f"{G}Enter new password: {W}")
    conf = getpass.getpass(f"{G}Confirm new password: {W}")
    if new != conf:
        print(f"{R}Passwords do not match!{W}")
        return
    save_pass(hash_pass(new))
    print(f"{G}✅ Password changed successfully.{W}")

# === MANUAL LOCK ===
def lock_now():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(BANNER)
    print(f"{Y}🔒 Lock activated manually. Please reauthenticate.{W}\n")
    main(auth_flow=True)

# === MAIN AUTH FLOW ===
def main(auth_flow=False):
    if not auth_flow:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print(BANNER)

    data = load_pass()
    if not data:
        print(f"{Y}No password set. Creating a new one...{W}")
        new = getpass.getpass(f"{G}Set a password: {W}")
        conf = getpass.getpass(f"{G}Confirm password: {W}")
        if new != conf:
            print(f"{R}Passwords do not match!{W}")
            return
        save_pass(hash_pass(new))
        print(f"{G}Password created successfully! Restart Termux to lock.{W}")
        return

    attempts = 0
    while True:
        username = input(f"{C}Enter username: {W}").strip()
        pwd = getpass.getpass(f"{Y}Enter password: {W}")

        if verify_pass(pwd, data):
            progress()
            welcome_message()
            # ensure terminal is left in a clean state before returning to shell
            sys.stdout.write("\n")
            sys.stdout.flush()
            break
        else:
            attempts += 1
            log_intruder(username)
            print(f"{R}Access Denied! Intruder Logged.{W}")
            if attempts >= 3:
                fake_delay_animated()
                attempts = 0

# === ENTRY POINT ===
if __name__ == '__main__':
    if '--change-password' in sys.argv:
        change_password()
    elif '--lock' in sys.argv:
        lock_now()
    else:
        main()
