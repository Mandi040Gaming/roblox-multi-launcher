# ❓ Error Guide — All Known Errors & Fixes

This document lists every known error that can occur when using the Roblox Multi-Account Launcher, along with the cause and step-by-step fix.

---

## Table of Contents

- [Roblox Errors](#-roblox-errors)
  - [Roblox encountered an unexpected error](#1-roblox-encountered-an-unexpected-error)
  - [Failed to create temporary file for dump creation](#2-failed-to-create-temporary-file-for-dump-creation)
  - [Roblox opens but stays on the home screen](#3-roblox-opens-but-stays-on-the-home-screen)
  - [All instances are logged in as the same account](#4-all-instances-are-logged-in-as-the-same-account)
  - [Roblox closes immediately after opening](#5-roblox-closes-immediately-after-opening)
- [Launcher Errors](#-launcher-errors)
  - [Auth ticket failed](#6-auth-ticket-failed)
  - [RobloxPlayerBeta.exe not found](#7-robloxplayerbetaexe-not-found)
  - [Invalid cookie / Cookie could not be validated](#8-invalid-cookie--cookie-could-not-be-validated)
  - [Missing packages / Dependencies missing](#9-missing-packages--dependencies-missing)
  - [Encryption error / Failed to decrypt](#10-encryption-error--failed-to-decrypt)
- [Windows / System Errors](#-windows--system-errors)
  - [Windows Defender / Antivirus warning](#11-windows-defender--antivirus-warning)
  - [mklink failed / Junction could not be created](#12-mklink-failed--junction-could-not-be-created)
  - [Permission denied / Access is denied](#13-permission-denied--access-is-denied)
  - [Python not found / 'python' is not recognized](#14-python-not-found--python-is-not-recognized)

---

## 🔴 Roblox Errors

These errors come from Roblox itself, not the launcher.

---

### 1. Roblox encountered an unexpected error

```
Roblox encountered an unexpected error.
Click 'OK' to create support files, then please share it on our site: https://roblox.com/support
```

**Cause:**
Roblox crashed during startup — most commonly caused by an invalid `TEMP` directory path or a corrupted per-account profile folder.

**Fix:**
1. Make sure you are on the **latest version** of `roblox_launcher.py` (download from [Releases](https://github.com/Mandi040Gaming/roblox-multi-launcher/releases))
2. This specific crash was fixed in **v3.0** — the `TEMP` variable now correctly points to the real Windows system temp folder
3. If it still happens, delete the profile folder for the affected account:
   - Open `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\` in Explorer
   - Delete the folder `acc_X` (where X is the account number)
   - Relaunch — the profile will be recreated automatically
4. If none of the above helps, try reinstalling Roblox via Bloxstrap

---

### 2. Failed to create temporary file for dump creation

```
Failed to create temporary file for dump creation.
Error: Der Verzeichnisname ist ungueltig (directory name is invalid)
```

**Cause:**
Roblox tried to write a crash dump to the `TEMP` folder, but the path set by the launcher was too long or contained characters that Windows does not accept for temp files.

**Fix:**
1. Update to the **latest version** of `roblox_launcher.py` — this was fixed in **v3.0**
2. `TEMP` and `TMP` now point to the real Windows system temp (`C:\Users\...\AppData\Local\Temp`) instead of a per-profile path
3. Simply redownload `roblox_launcher.py` from [Releases](https://github.com/Mandi040Gaming/roblox-multi-launcher/releases) and replace your existing file

---

### 3. Roblox opens but stays on the home screen / no game joins

**Cause:**
This is **expected behaviour** — the launcher starts Roblox without a target game or Place ID.

**Fix:**
- After Roblox loads, join any game manually from the home screen
- A future version may support launching directly into a specific Place ID

---

### 4. All instances are logged in as the same account

**Cause:**
Each account card must have its own unique `.ROBLOSECURITY` cookie from a separate browser session. If you copied the same cookie for multiple accounts, they will all log in as that one account.

**Fix:**
1. Open your browser and log in as Account A → copy the cookie
2. Add Account A in the launcher with that cookie
3. Log out of Account A in the browser → log in as Account B → copy that cookie
4. Add Account B with the new cookie
5. Repeat for each account — every cookie must be unique

Alternatively, use **separate browser profiles** (Chrome: three-dot menu → Profiles → Add) so you can be logged into multiple accounts at once.

---

### 5. Roblox closes immediately after opening

**Cause:**
Several possible causes: corrupted profile, outdated Roblox version, or the auth ticket expired before Roblox could use it.

**Fix:**
1. Delete the profile for the affected account: `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\acc_X\`
2. Open Bloxstrap normally and let it update Roblox to the latest version
3. Try launching the account again — if the ticket expires too fast, the 8-second delay between starts should prevent this
4. If only one specific account has this issue, delete and re-add it with a fresh cookie

---

## 🟡 Launcher Errors

These errors are shown directly inside the launcher.

---

### 6. Auth ticket failed

```
Auth ticket failed — check the console for details
```

**Cause:**
The launcher could not obtain a one-time auth ticket from the Roblox API (`auth.roblox.com/v1/authentication-ticket`).

**Fix:**
1. **Expired cookie** (most common) — Roblox cookies last ~30 days. Delete the account and re-add it with a freshly copied cookie
2. Run the launcher from a terminal to see the full API response:
   ```
   python roblox_launcher.py
   ```
   Look for lines starting with `[Auth]` — they show exactly which step failed
3. Check your internet connection — `auth.roblox.com` must be reachable
4. If Roblox's API is down or rate-limiting your IP, wait a few minutes and try again
5. Make sure the full cookie was pasted — it must start with `_|WARNING:-DO-NOT-SHARE-THIS`

---

### 7. RobloxPlayerBeta.exe not found

```
RobloxPlayerBeta.exe not found
```

**Cause:**
The launcher searched in all known Roblox install locations but could not find the executable.

**Fix:**
1. Open Bloxstrap and click **"Launch Roblox"** at least once — this downloads and installs `RobloxPlayerBeta.exe`
2. The launcher searches in these locations (in order):
   - `%LOCALAPPDATA%\Bloxstrap\Versions\`
   - `%LOCALAPPDATA%\Roblox\Versions\`
3. If Roblox is installed somewhere else, reinstall it through Bloxstrap to ensure it ends up in the expected location

---

### 8. Invalid cookie / Cookie could not be validated

```
The cookie could not be validated. It may have expired or was copied incorrectly.
```

**Cause:**
The Roblox Users API rejected the cookie — it is either expired, incomplete, or belongs to a banned/deleted account.

**Fix:**
1. Go to [roblox.com](https://www.roblox.com) and make sure you are logged in as the correct account
2. Re-copy the cookie — ensure you copy the **entire value** (starts with `_|WARNING:`, ~600 characters)
3. If the account was recently created, wait a few minutes before copying the cookie
4. If your IP is temporarily blocked by Roblox, try again later or use a different network

---

### 9. Missing packages / Dependencies missing

```
The following packages are missing: requests, cryptography, Pillow
```

**Cause:**
Python dependencies are not installed.

**Fix:**
1. The launcher offers to install them automatically — click **Yes**
2. If auto-install fails, open a terminal and run:
   ```
   pip install requests cryptography Pillow
   ```
3. If `pip` is not found, reinstall Python and make sure **"Add Python to PATH"** is checked during installation

---

### 10. Encryption error / Failed to decrypt

```
cryptography.fernet.InvalidToken
```

**Cause:**
The encryption key (`.key` file) no longer matches the stored encrypted cookies — this happens if the `.key` file was deleted or replaced.

**Fix:**
1. All stored accounts need to be re-added — the old encrypted data cannot be recovered without the original key
2. Delete `%LOCALAPPDATA%\RobloxMultiLauncher\accounts.json` and `%LOCALAPPDATA%\RobloxMultiLauncher\.key`
3. Restart the launcher — a new key will be generated
4. Re-add all accounts with fresh cookies

> ⚠️ Never delete the `.key` file while you still have accounts saved — always remove accounts first via the launcher UI.

---

## 🔵 Windows / System Errors

---

### 11. Windows Defender / Antivirus warning

```
Windows protected your PC
This app might put your PC at risk
```

**Cause:**
The script is unsigned, and it uses Windows APIs (registry, kernel32 mutex, subprocess) that trigger heuristic detection in some antivirus programs.

**Fix:**
1. Click **"More info"** → **"Run anyway"** in the Windows SmartScreen dialog
2. The full source code is in `roblox_launcher.py` — you can review every line before running
3. If your antivirus quarantines the file, add an exception for the folder containing `roblox_launcher.py`
4. Nothing in this tool connects to any server except Roblox's official API endpoints

---

### 12. mklink failed / Junction could not be created

**Cause:**
Windows could not create a directory junction (symlink) from the fake profile Versions folder to the real Roblox Versions folder. This usually happens due to missing permissions or the junction already existing in a broken state.

**Fix:**
1. Run `start.bat` as **Administrator** (right-click → Run as administrator) at least once to create the junction
2. If the junction is broken, delete the `Versions` folder inside the affected profile:
   - `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\acc_X\LocalAppData\Roblox\Versions`
3. Relaunch — it will be recreated automatically

---

### 13. Permission denied / Access is denied

**Cause:**
The launcher does not have write access to the profile directory or registry key.

**Fix:**
1. Make sure `%LOCALAPPDATA%` is writable — this is your personal user folder and should always be writable
2. Try running `start.bat` as Administrator
3. Check if any other program (antivirus, backup tool) is locking the files

---

### 14. Python not found / 'python' is not recognized

```
'python' is not recognized as an internal or external command
```

**Cause:**
Python is not installed, or was installed without being added to the system PATH.

**Fix:**
1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. During installation: ✅ check **"Add Python to PATH"** before clicking Install Now
3. After installing, close and reopen any terminal windows, then run `start.bat` again
4. To verify Python is on PATH, open a terminal and run: `python --version`

---

## 💡 General Tips

- **Always use the latest release** — many errors were fixed in newer versions. Download from [github.com/Mandi040Gaming/roblox-multi-launcher/releases](https://github.com/Mandi040Gaming/roblox-multi-launcher/releases)
- **Run from a terminal** (`python roblox_launcher.py`) to see detailed `[Auth]` debug output when troubleshooting
- **Cookies expire** after ~30 days — if things suddenly stop working, refreshing all cookies is the first thing to try
- **Profile folders** at `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\` can always be safely deleted and will be recreated on next launch

---

*Still stuck? Open an issue at [github.com/Mandi040Gaming/roblox-multi-launcher/issues](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues)*
