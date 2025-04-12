# 🛠 Debian-Based OS with GUI 

This project is a custom Debian-based operating system built using **live-build**, featuring:
- Xorg and Openbox window manager
- A **custom PyQt login screen** replacing the default CLI login
- Autologin handled via systemd
- User switching to full shell or GUI session

![Alt text](diagram.png)

---

## 📁 Directory Structure

```
project-root/
├── config/
│   ├── includes.chroot/               # Files copied to filesystem before build
│   │   ├── etc/skel/.xinitrc          # User's xinitrc for X session
│   │   └── usr/local/bin/             # Custom scripts
│   │       ├── gui-login-x.sh         # Script for launching X + login
│   │       └── switch-user.sh         # Script for switching to the user
│   └── package-lists/                 # Custom packages to install
├── hooks/
│   └── ...                            # Optional pre/post build hooks
```

---

## 🚀 How It Works

### Boot Process Flow:
1. System boots to `multi-user.target`.
2. systemd starts `login-gui.service`.
3. `login-gui.service` runs `gui-login-x.sh`.
4. That script:
   - Detects the first valid user dynamically.
   - Starts the X session via `xinit` using the user’s `.xinitrc`.
   - `.xinitrc` launches `openbox` and the PyQt login screen.
5. After successful login:
   - `switch-user.sh` is called to switch from root to the selected user.
   - Shell session (CLI/GUI) starts.

---



---

## 🧼 Clean Build Environment
If changes any config files
```bash
sudo lb config
```

Before rebuilding:

```bash
sudo lb clean
```

To clean everything:
```bash
sudo lb clean --purge
```

---

## 🏗 Build the ISO

```bash
sudo lb build
```

Generated ISO will be located in the project root directory.

---

## 📋 Notes

- No use of `sudo` inside scripts or setup (OS-level configuration).
- GUI login screen is purely custom and replaces default `getty`.
- No static users created — system dynamically handles user detection.
- Use `.xinitrc` under `/etc/skel` to prepopulate new user configs.
