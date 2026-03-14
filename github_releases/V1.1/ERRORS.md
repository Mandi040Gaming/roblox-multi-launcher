# ❓ Error Guide — All Known Errors & Fixes

**Version:** V1.1  
**Repository:** [github.com/Mandi040Gaming/roblox-multi-launcher](https://github.com/Mandi040Gaming/roblox-multi-launcher)  
**Latest release:** [github_releases/V1.1](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1)

> 💡 **Before doing anything else:** make sure you are running **V1.1**. Many errors listed here were already fixed in this version. Download it at the link above.

---

## Table of Contents

- [🔴 Roblox Errors](#-roblox-errors)
  - [1. Roblox encountered an unexpected error](#1-roblox-encountered-an-unexpected-error)
  - [2. Failed to create temporary file for dump creation](#2-failed-to-create-temporary-file-for-dump-creation)
  - [3. Roblox opens but stays on the home screen](#3-roblox-opens-but-stays-on-the-home-screen)
  - [4. All instances are logged in as the same account](#4-all-instances-are-logged-in-as-the-same-account)
  - [5. Roblox closes immediately after opening](#5-roblox-closes-immediately-after-opening)
- [🟡 Launcher Errors](#-launcher-errors)
  - [6. Auth ticket failed](#6-auth-ticket-failed)
  - [7. RobloxPlayerBeta.exe not found](#7-robloxplayerbetaexe-not-found)
  - [8. Invalid cookie / Cookie could not be validated](#8-invalid-cookie--cookie-could-not-be-validated)
  - [9. Missing packages / Dependencies missing](#9-missing-packages--dependencies-missing)
  - [10. Encryption error / Failed to decrypt](#10-encryption-error--failed-to-decrypt)
- [🔵 Windows / System Errors](#-windows--system-errors)
  - [11. Windows Defender / Antivirus warning](#11-windows-defender--antivirus-warning)
  - [12. mklink failed / Junction could not be created](#12-mklink-failed--junction-could-not-be-created)
  - [13. Permission denied / Access is denied](#13-permission-denied--access-is-denied)
  - [14. Python not found / 'python' is not recognized](#14-python-not-found--python-is-not-recognized)
- [💡 General Tips](#-general-tips)

---

## 🔴 Roblox Errors

These error dialogs come from Roblox itself.

---

### 1. Roblox encountered an unexpected error

```
Roblox encountered an unexpected error.
Click 'OK' to create support files, then please share it on our site: https://roblox.com/support
```

**Status:** ✅ Fixed in V1.1

**Cause:**
Roblox crashed during startup — most commonly because the `TEMP` environment variable pointed to a deep custom path that Roblox could not write crash dumps to.

**Fix:**
1. Update to **[V1.1](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1)** — `TEMP` and `TMP` now point to the real Windows system temp directory
2. If it still happens after updating, delete the profile for the affected account:
   - Open `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\` in Explorer
   - Delete the folder `acc_X` (replace X with the account number shown in the launcher)
   - Relaunch the account — the profile is recreated automatically
3. If the issue persists, open Bloxstrap and run **"Repair Roblox"** to rule out a corrupted installation

---

### 2. Failed to create temporary file for dump creation

```
Failed to create temporary file for dump creation.
Error: Der Verzeichnisname ist ungueltig (directory name is invalid)
```

**Status:** ✅ Fixed in V1.1

**Cause:**
Roblox tried to write a crash dump file but the `TEMP` path set by an older version of the launcher was too long or contained characters that Windows rejects for temporary files.

**Fix:**
1. Download **[V1.1](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1)** and replace your existing `roblox_launcher.py`
2. `TEMP` and `TMP` are now left as the real Windows system temp — this error cannot occur in V1.1

---

### 3. Roblox opens but stays on the home screen

**Status:** ℹ️ Expected behaviour

**Cause:**
The launcher starts Roblox without a specific game or Place ID target — Roblox lands on the home screen just like a normal launch.

**Fix:**
- Join any game manually from the Roblox home screen after the client finishes loading
- This is intentional — a future version may add support for launching directly into a specific Place ID

---

### 4. All instances are logged in as the same account

**Status:** ℹ️ User configuration issue

**Cause:**
Each account in the launcher must have its own unique `.ROBLOSECURITY` cookie from a separate browser session. If the same cookie was saved for multiple accounts, all instances will log in as that one account.

**Fix:**
1. Open your browser and log in as **Account A** → copy the cookie → add it to the launcher
2. Log out in the browser → log in as **Account B** → copy that cookie → add it
3. Repeat for every account — every cookie must be unique and come from a different login session

**Tip:** Use separate **browser profiles** (Chrome: three-dot menu → Profiles → Add new profile) so you can stay logged into multiple Roblox accounts at once without logging out.

---

### 5. Roblox closes immediately after opening

**Status:** ⚠️ Multiple possible causes

**Cause:**
Could be a corrupted profile folder, an expired auth ticket, or an outdated Roblox installation.

**Fix:**
1. Delete the profile folder for the affected account: `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\acc_X\`
2. Open Bloxstrap and launch Roblox normally once — this ensures the latest version is installed
3. Re-add the account in the launcher with a fresh cookie, then try again
4. If multiple accounts have this issue, make sure you are on **V1.1**

---

## 🟡 Launcher Errors

These messages appear inside the launcher UI or in the terminal.

---

### 6. Auth ticket failed

```
Auth ticket failed — check the console for details
```

**Cause:**
The launcher could not get a one-time auth ticket from `auth.roblox.com/v1/authentication-ticket`.

**Fix:**
1. **Most common cause — expired cookie:** Roblox cookies last ~30 days. Delete the account in the launcher and re-add it with a freshly copied cookie
2. Run the launcher from a terminal to see the full debug output:
   ```
   python roblox_launcher.py
   ```
   Look for lines starting with `[Auth]` — they show the exact API step that failed and the HTTP status code
3. Check your internet connection — `auth.roblox.com` must be reachable
4. If Roblox's servers are down or rate-limiting your IP, wait a few minutes and try again
5. Make sure the cookie was pasted in full — it must start with `_|WARNING:-DO-NOT-SHARE-THIS`

**Example of healthy console output:**
```
[Auth] Step1 status: 403
[Auth] CSRF token: T7xK3m...
[Auth] Step2 status: 200
[Auth] Ticket OK: eyJhbGci...
```
If Step1 returns `401`, the cookie is invalid or expired. If Step2 returns anything other than `200`, the API may be temporarily unavailable.

---

### 7. RobloxPlayerBeta.exe not found

```
RobloxPlayerBeta.exe not found
```

**Cause:**
The launcher searched all known install locations but could not find the Roblox player executable.

**Fix:**
1. Open **Bloxstrap** and click **"Launch Roblox"** — this downloads and installs `RobloxPlayerBeta.exe` if it is missing
2. The launcher searches these paths (in order):
   - `%LOCALAPPDATA%\Bloxstrap\Versions\`
   - `%LOCALAPPDATA%\Roblox\Versions\`
3. If Roblox was installed to a non-standard location, reinstall it via Bloxstrap to put it in the expected place

---

### 8. Invalid cookie / Cookie could not be validated

```
The cookie could not be validated. It may have expired or was copied incorrectly.
```

**Cause:**
The Roblox Users API rejected the cookie — it is expired, incomplete, or belongs to a banned/deleted account.

**Fix:**
1. Make sure you are logged into the **correct account** on roblox.com before copying
2. Copy the **entire** cookie value — it starts with `_|WARNING:` and is approximately 600 characters long
3. If the account was recently created or recently logged in, wait a minute and try again
4. If your IP is temporarily rate-limited by Roblox, wait a few minutes or switch networks

---

### 9. Missing packages / Dependencies missing

```
The following packages are missing: requests, cryptography, Pillow
```

**Cause:**
The required Python packages are not installed in your Python environment.

**Fix:**
1. Click **Yes** when the launcher offers to install them automatically
2. If auto-install fails, open a terminal (Win+R → `cmd`) and run:
   ```
   pip install requests cryptography Pillow
   ```
3. If `pip` is not found, reinstall Python from [python.org](https://www.python.org/downloads/) and make sure **"Add Python to PATH"** is checked during setup

---

### 10. Encryption error / Failed to decrypt

```
cryptography.fernet.InvalidToken
```

**Cause:**
The `.key` encryption file no longer matches the stored encrypted cookies. This happens if the `.key` file was deleted, replaced, or moved.

**Fix:**
1. All stored accounts must be re-added — encrypted data cannot be recovered without the original key
2. Delete both files:
   - `%LOCALAPPDATA%\RobloxMultiLauncher\accounts.json`
   - `%LOCALAPPDATA%\RobloxMultiLauncher\.key`
3. Restart the launcher — a new key is generated automatically
4. Re-add all accounts with fresh cookies

> ⚠️ Never manually delete or move the `.key` file while accounts are still saved. Always remove accounts through the launcher UI first.

---

## 🔵 Windows / System Errors

---

### 11. Windows Defender / Antivirus warning

```
Windows protected your PC — Microsoft Defender SmartScreen prevented an unrecognized app from starting.
```

**Cause:**
The script is unsigned. It uses Windows APIs (registry access, kernel32 mutex, subprocess) that can trigger heuristic detection in some antivirus programs.

**Fix:**
1. Click **"More info"** → **"Run anyway"** in the SmartScreen dialog
2. The complete source code is in `roblox_launcher.py` — every line is readable and reviewable
3. The only external connections made are to official Roblox API endpoints (`roblox.com`, `auth.roblox.com`, `users.roblox.com`, `thumbnails.roblox.com`)
4. If your antivirus quarantines the file, add an exception for the folder containing `roblox_launcher.py`

---

### 12. mklink failed / Junction could not be created

**Cause:**
Windows could not create a directory junction from the fake profile Versions folder to the real Roblox Versions folder. Usually a permissions issue or a leftover broken junction.

**Fix:**
1. Run `start.bat` as **Administrator** (right-click → Run as administrator) at least once
2. If the junction is in a broken state, delete the Versions folder inside the affected profile:
   ```
   %LOCALAPPDATA%\RobloxMultiLauncher\profiles\acc_X\LocalAppData\Roblox\Versions
   ```
3. Relaunch the account — the junction will be recreated

---

### 13. Permission denied / Access is denied

**Cause:**
The launcher does not have write permission to the profile directory or the Windows registry key.

**Fix:**
1. `%LOCALAPPDATA%` is your personal user folder and should always be writable — if it is not, check your Windows user account permissions
2. Try running `start.bat` as **Administrator**
3. Check if an antivirus or backup program is locking the files in the profile directory

---

### 14. Python not found / 'python' is not recognized

```
'python' is not recognized as an internal or external command, operable program or batch file.
```

**Cause:**
Python is not installed, or was installed without being added to the system `PATH`.

**Fix:**
1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. During installation: ✅ check **"Add Python to PATH"** before clicking Install Now — this step is easy to miss
3. After installing, close all terminal windows and run `start.bat` again
4. To verify Python is accessible, open a new terminal and run:
   ```
   python --version
   ```
   You should see something like `Python 3.11.9`

---

## 💡 General Tips

- **Always use the latest version** — download from [github_releases/V1.1](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1). When a newer version appears in `github_releases/`, download that one instead.
- **Run from a terminal** when troubleshooting — open `cmd`, navigate to the launcher folder, and run `python roblox_launcher.py` to see full `[Auth]` debug output
- **Cookies expire** after ~30 days — if everything was working and suddenly stops, refreshing all cookies is almost always the fix
- **Profile folders** at `%LOCALAPPDATA%\RobloxMultiLauncher\profiles\` can always be safely deleted and will be recreated on the next launch
- **8-second delay** between account starts is intentional — it ensures each account gets a clean, isolated login without cookie conflicts

---

*Still stuck? Open an issue at [github.com/Mandi040Gaming/roblox-multi-launcher/issues](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues)*
