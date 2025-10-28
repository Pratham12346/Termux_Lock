# Termux Lock — Advanced Edition (Pratham)

A compact, stylish Termux lock with:

- Username + password authentication (PBKDF2)
- Manual lock command (`termux-lock`)
- Animated fake delay after repeated failures
- Welcome message with system info after successful unlock
- Autostart on Termux start

## Install

```bash
pkg update -y
pkg install -y python
# copy or clone this repo into your device, then:
cd <repo-folder>
python3 install.py
```

Restart Termux to see the lock. To test manually:

```bash
python3 ~/.termux_lock/termux_lock.py
```

## Commands
- `termux-lock` — immediately lock the session
- `python3 ~/.termux_lock/termux_lock.py --change-password` — change password

## Notes
This lock is a convenience layer — anyone with filesystem or root access can remove/modify it.

Made by Pratham (Hackerk_17)
