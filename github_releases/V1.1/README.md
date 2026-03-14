<div align="center">

# 🎮 Roblox Multi-Account Launcher

**Launch multiple Roblox accounts simultaneously — no switching, no hassle.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Bloxstrap](https://img.shields.io/badge/Requires-Bloxstrap-7c3aed)](https://github.com/bloxstraplabs/bloxstrap/releases)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

[**Releases**](https://github.com/Mandi040Gaming/roblox-multi-launcher/releases) · [**Error Guide**](ERRORS.md) · [**Report a Bug**](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues) · [**Request a Feature**](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues)

</div>

---

## ✨ Features

- 🔀 **True multi-instance** — run 2, 3, 4+ Roblox accounts at the same time
- 🎫 **Auth-Ticket login** — each account logs in cleanly via Roblox's own API, no manual switching required
- 🛡️ **Encrypted storage** — cookies are stored locally using Fernet encryption and never sent anywhere
- 🖼️ **Profile avatars** — automatically fetches and displays each account's Roblox headshot
- 🎨 **Clean dark UI** — minimal, fast tkinter interface
- 🔒 **Cookie-only** — no passwords stored, ever

---

## 📥 Download

> ⚠️ **Always download the latest release** — older versions may have bugs that have already been fixed.

1. Go to [**Releases**](https://github.com/Mandi040Gaming/roblox-multi-launcher/releases)
2. Click the latest release at the top
3. Under **Assets**, download **`roblox-multi-launcher-vX.X.zip`**
4. Extract the ZIP and run **`start.bat`**

The releases are located in the [`github_releases/`](github_releases/) folder of this repository and are also published as GitHub Releases for easy download.

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

### Step 3 — Download the launcher

1. Go to [**Releases**](https://github.com/Mandi040Gaming/roblox-multi-launcher/releases) and download the latest ZIP
2. Extract it to any folder on your PC

### Step 4 — Run

Double-click **`start.bat`** — it will automatically install all Python dependencies and launch the tool.

> 💡 On first launch, Windows Defender may show a warning. Click **"More info" → "Run anyway"**. The full source code is in `roblox_launcher.py` for review.

---

## 🍪 How to get your `.ROBLOSECURITY` Cookie

The tool authenticates via your browser cookie — no password is ever stored or transmitted.

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

### Cookie-Editor Extension (easiest)

1. Install [Cookie-Editor](https://cookie-editor.com) from the Chrome Web Store or Firefox Add-ons
2. Go to roblox.com while logged in → click the Cookie-Editor icon
3. Find `.ROBLOSECURITY` → copy the value

> ⚠️ The cookie starts with `_|WARNING:-DO-NOT-SHARE...` and is ~600 characters long. Copy the **entire value**. Cookies expire after ~30 days.

---

## 📖 Usage

1. **Add an account** — Click **"➕ Add Account"**, enter a display name and paste the cookie
2. **Select accounts** — Click cards to select them (highlighted in blue)
3. **Launch selected** — Click **"▶ Launch Selected"** or double-click a card to launch immediately
4. **Launch all** — Click **"▶▶ Launch All"** to start every account at once

> Each account starts with an **8-second delay** between instances to ensure clean, isolated login.

---

## 🗂️ Repository Structure

```
roblox-multi-launcher/
│
├── github_releases/           ← All versioned releases live here
│   ├── v3.0/
│   │   ├── roblox_launcher.py
│   │   ├── start.bat
│   │   └── README.md
│   └── ...
│
├── roblox_launcher.py         ← Latest version of the main app
├── start.bat                  ← Run this to launch
├── README.md                  ← This file
├── ERRORS.md                  ← Full error guide
├── LICENSE
└── .gitignore
```

> 💡 The `github_releases/` folder contains all past and current versioned releases. **Always use the latest one** — older releases may have known bugs that have been fixed.

**App data stored locally at `%LOCALAPPDATA%\RobloxMultiLauncher\`:**
```
RobloxMultiLauncher/
├── accounts.json          ← Encrypted account list
├── .key                   ← Encryption key (never share or commit this!)
├── profiles/              ← Isolated per-account Roblox profiles
│   └── acc_1/
│       └── LocalAppData/
└── avatars/               ← Cached profile picture PNGs
```

---

## 🔧 How It Works

1. **Cookie validation** — The cookie is verified against `users.roblox.com/v1/users/authenticated`
2. **Auth Ticket** — A short-lived token is fetched from `auth.roblox.com/v1/authentication-ticket` using a two-step CSRF flow
3. **Isolated profiles** — Each account gets its own `LOCALAPPDATA` via environment variables, preventing session conflicts
4. **Mutex bypass** — The launcher holds the `ROBLOX_singletonEvent` Windows mutex, allowing multiple instances to run simultaneously
5. **Direct launch** — `RobloxPlayerBeta.exe` is started with the auth ticket URI, bypassing Bloxstrap's menu entirely

---

## ❓ Errors & Troubleshooting

For a full list of every known error with causes and step-by-step fixes, see **[ERRORS.md](ERRORS.md)**.

**Quick reference:**

| Error | Fix |
|-------|-----|
| `Roblox encountered an unexpected error` | Update to latest version, delete profile folder for that account |
| `Failed to create temporary file for dump creation` | Update to latest version (fixed in v3.0) |
| `Auth ticket failed` | Cookie expired — re-add account with a fresh cookie |
| `RobloxPlayerBeta.exe not found` | Launch Roblox once via Bloxstrap |
| `Invalid cookie` | Copy the full cookie value again from your browser |
| `Python is not recognized` | Reinstall Python with "Add to PATH" checked |
| All accounts log in as the same user | Each account needs its own unique cookie |

---

## ⚖️ Legal & Disclaimer

- This project is **not affiliated with, endorsed by, or connected to Roblox Corporation**
- Use is **at your own risk** — multi-account usage may violate [Roblox's Terms of Service](https://en.help.roblox.com/hc/en-us/articles/115004647846)
- All data is stored **locally only** — nothing is uploaded or shared
- The author is not responsible for any bans or consequences from using this tool

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
