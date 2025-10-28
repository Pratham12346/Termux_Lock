#!/usr/bin/env python3
import os, shutil, stat, sys

HOME = os.path.expanduser("~")
# assume user runs install.py from the project folder
SRC_LOCK = os.path.join(os.getcwd(), "termux_lock.py")
DEST_DIR = os.path.join(HOME, ".termux_lock")
DEST_LOCK = os.path.join(DEST_DIR, "termux_lock.py")

os.makedirs(DEST_DIR, exist_ok=True)

# Copy (replace existing)
if os.path.exists(DEST_LOCK):
    print("🔁 Updating existing Termux Lock...")
    os.remove(DEST_LOCK)

shutil.copy2(SRC_LOCK, DEST_LOCK)
os.chmod(DEST_LOCK, stat.S_IRWXU)

# Setup autostart in .bash_profile/.bashrc
bashrc = os.path.join(HOME, ".bashrc")
bash_profile = os.path.join(HOME, ".bash_profile")
start_line = "python3 ~/.termux_lock/termux_lock.py\\n"
alias_line = "alias termux-lock='python3 ~/.termux_lock/termux_lock.py --lock'\\n"

# ensure .bash_profile sources .bashrc
if not os.path.exists(bash_profile):
    with open(bash_profile, "w") as f:
        f.write("if [ -f ~/.bashrc ]; then . ~/.bashrc; fi\\n")

# add start_line if missing
if os.path.exists(bashrc):
    with open(bashrc, "r+") as f:
        content = f.read()
        if start_line not in content:
            f.write("\\n# Termux Lock autostart\\n" + start_line)
        if alias_line not in content:
            f.write(alias_line)
else:
    with open(bashrc, "w") as f:
        f.write("# Termux Lock autostart\\n" + start_line + alias_line)

print("✅ Termux Lock installed to ~/.termux_lock/")
print("🔒 Autostart added to ~/.bashrc (and ~/.bash_profile if needed)")
print("💡 Use 'termux-lock' to lock manually or restart Termux to test the lock.")