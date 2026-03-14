<div align="center">

# 🎮 Roblox Multi-Account Launcher

**Launch multiple Roblox accounts simultaneously — no switching, no hassle.**

[![Version](https://img.shields.io/badge/Version-1.1-3b82f6)](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Bloxstrap](https://img.shields.io/badge/Requires-Bloxstrap-7c3aed)](https://github.com/bloxstraplabs/bloxstrap/releases)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

[**⬇ Download V1.1**](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1) · [**❓ Error Guide**](ERRORS.md) · [**🐛 Report a Bug**](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues) · [**💡 Request a Feature**](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues)

</div>

---

## 📥 Download

> ⚠️ **Always use the latest release.** Older versions may contain bugs that have already been fixed.

The latest release is **V1.1** — download it here:

👉 **[github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1)**

All releases are archived in the [`github_releases/`](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases) folder of this repository. When a new version is released, a new subfolder (e.g. `V1.2`, `V2.0`) will appear there — always grab the highest version number.

---

## ✨ Features

- 🔀 **True multi-instance** — run 2, 3, 4+ Roblox accounts at the same time
- 🎫 **Auth-Ticket login** — each account logs in cleanly via Roblox's own API, no manual switching required
- 🛡️ **Encrypted storage** — cookies are stored locally with Fernet encryption and never sent anywhere
- 🖼️ **Profile avatars** — automatically fetches and displays each account's Roblox headshot
- 🎨 **Clean dark UI** — minimal, fast tkinter interface
- 🔒 **Cookie-only** — no passwords stored, ever

---

## 📋 Requirements

| Requirement | Version | Download |
|-------------|---------|----------|
| **Windows** | 10 or 11 (64-bit) | — |
| **Python** | 3.11 or newer | [python.org](https://www.python.org/downloads/) |
| **Bloxstrap** | Latest | [bloxstraplabs/bloxstrap](https://github.com/bloxstraplabs/bloxstrap/releases) |

> ⚠️ **Roblox must have been launched at least once via Bloxstrap** before using this tool, so that `RobloxPlayerBeta.exe` is present on your system.

---

## 🚀 Installation

### Step 1 — Install Python

1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **Check "Add Python to PATH"** — this is required!
4. Click **Install Now**

### Step 2 — Install Bloxstrap & Roblox

1. Download Bloxstrap from [github.com/bloxstraplabs/bloxstrap/releases](https://github.com/bloxstraplabs/bloxstrap/releases)
2. Run `Bloxstrap.exe` and let it install Roblox
3. Launch Roblox at least once through Bloxstrap so all files are downloaded

### Step 3 — Download V1.1

1. Go to **[github_releases/V1.1](https://github.com/Mandi040Gaming/roblox-multi-launcher/tree/main/github_releases/V1.1)**
2. Download all files from that folder (or clone the repo)
3. Extract / place them in any folder on your PC

### Step 4 — Run

Double-click **`start.bat`** — it automatically installs all Python dependencies and starts the launcher.

> 💡 Windows Defender may show a SmartScreen warning on first launch. Click **"More info" → "Run anyway"**. The full source is in `roblox_launcher.py` for anyone to review.

---

## 🍪 How to get your `.ROBLOSECURITY` Cookie

The launcher authenticates via your browser cookie — no password is ever stored or transmitted.

### Chrome / Edge / Brave

1. Go to [roblox.com](https://www.roblox.com) and log in with the account you want to add
2. Press **F12** → **Application** tab
3. Left panel: **Storage → Cookies → https://www.roblox.com**
4. Find **`.ROBLOSECURITY`** → double-click the Value cell → **Ctrl+A** → **Ctrl+C**
5. Paste into the Cookie field in the launcher

### Firefox

1. Go to [roblox.com](https://www.roblox.com) and log in → press **F12** → **Storage** tab
2. Left panel: **Cookies → https://www.roblox.com**
3. Click `.ROBLOSECURITY` → copy the value on the right

### Cookie-Editor Extension (easiest method)

1. Install [Cookie-Editor](https://cookie-editor.com) from the Chrome Web Store or Firefox Add-ons
2. Go to roblox.com while logged in → click the Cookie-Editor icon in the toolbar
3. Find `.ROBLOSECURITY` → click it → copy the value

> ⚠️ The cookie starts with `_|WARNING:-DO-NOT-SHARE...` and is ~600 characters long. Copy the **entire value**. Cookies expire after ~30 days and need to be refreshed.

---

## 📖 Usage

1. **Add an account** — Click **"➕ Add Account"** in the sidebar, enter a display name and paste the cookie
2. **Select accounts** — Click cards to select them (highlighted in blue)
3. **Launch selected** — Click **"▶ Launch Selected"** in the bottom bar, or double-click a card to launch it immediately
4. **Launch all** — Click **"▶▶ Launch All"** in the sidebar to start every account at once

> Each account starts with an **8-second delay** between instances to ensure clean, isolated login injection.

---

## 🗂️ Repository Structure

```
roblox-multi-launcher/
│
├── github_releases/                ← All versioned releases live here
│   ├── V1.0/                       ← Initial release
│   └── V1.1/                       ← Current release (latest)
│       ├── roblox_launcher.py
│       ├── start.bat
│       ├── README.md
│       └── ERRORS.md
│
├── README.md                       ← This file (mirrors latest release)
├── ERRORS.md                       ← Full error guide
├── LICENSE
└── .gitignore
```

> 💡 The root `roblox_launcher.py` and `README.md` always mirror the latest release. For an archived copy of a specific version, look inside `github_releases/VX.X/`.

**App data stored locally at `%LOCALAPPDATA%\RobloxMultiLauncher\`:**

```
RobloxMultiLauncher/
├── accounts.json       ← Encrypted account list
├── .key                ← Encryption key (never share or commit this!)
├── profiles/           ← Isolated per-account Roblox profile folders
│   └── acc_1/
│       └── LocalAppData/
└── avatars/            ← Cached profile picture PNGs
```

---

## 🔧 How It Works

1. **Cookie validation** — The cookie is checked against `users.roblox.com/v1/users/authenticated`
2. **Auth Ticket** — A short-lived one-time token is fetched from `auth.roblox.com/v1/authentication-ticket` via a two-step CSRF flow
3. **Isolated profiles** — Each account gets its own `LOCALAPPDATA` folder via environment variables, preventing session conflicts between instances
4. **Mutex bypass** — The launcher holds the `ROBLOX_singletonEvent` Windows mutex so multiple Roblox instances can run at the same time
5. **Direct launch** — `RobloxPlayerBeta.exe` is started with the auth ticket URI, bypassing Bloxstrap's interactive menu entirely

---

## ❓ Errors & Troubleshooting

For a full list of every known error with detailed causes and fixes, see **[ERRORS.md](ERRORS.md)**.

**Quick reference:**

| Error | Likely cause | Quick fix |
|-------|-------------|-----------|
| `Roblox encountered an unexpected error` | Corrupted profile or outdated version | Update to V1.1, delete profile folder for that account |
| `Failed to create temporary file for dump creation` | Invalid TEMP path (old bug) | Update to V1.1 — fixed |
| `Auth ticket failed` | Cookie expired | Re-add account with a fresh cookie |
| `RobloxPlayerBeta.exe not found` | Roblox not installed | Launch Roblox once via Bloxstrap |
| `Invalid cookie` | Incomplete or expired cookie | Re-copy the full cookie from your browser |
| `Python is not recognized` | Python not on PATH | Reinstall Python, check "Add to PATH" |
| All accounts log in as the same user | Same cookie used for multiple accounts | Each account needs its own unique cookie |

---

## 📋 Changelog

### V1.1 — Current
- Fixed: `TEMP`/`TMP` now use the real Windows system temp directory, preventing the *"Failed to create temporary file"* crash
- Fixed: Roblox no longer shows an unexpected error dialog on startup
- Improved: Auth ticket flow now uses correct two-step CSRF handling
- Improved: All UI text and code fully in English
- Added: `ERRORS.md` with a full list of known errors and fixes

### V1.0 — Initial Release
- Multi-account launch via isolated LOCALAPPDATA profiles
- Cookie-only login with Fernet encryption
- Auth-Ticket inject via Roblox API
- Singleton mutex bypass for multi-instance support
- Avatar loading, dark UI, search, account management

---

## ⚖️ Legal & Disclaimer

- This project is **not affiliated with, endorsed by, or connected to Roblox Corporation** in any way
- Use is **at your own risk** — multi-account usage may violate [Roblox's Terms of Service](https://en.help.roblox.com/hc/en-us/articles/115004647846)
- All data is stored **locally on your machine only** — nothing is uploaded, logged, or transmitted to any third party
- The author is not responsible for any account bans or other consequences from using this tool

---

## 📄 License

[MIT License](LICENSE)

---

## 🤝 Contributing

1. Fork the repo at [github.com/Mandi040Gaming/roblox-multi-launcher](https://github.com/Mandi040Gaming/roblox-multi-launcher)
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

<div align="center">
Made with ❤️ &nbsp;—&nbsp; If this helped you, leave a ⭐ on <a href="https://github.com/Mandi040Gaming/roblox-multi-launcher">GitHub</a>!
</div>
