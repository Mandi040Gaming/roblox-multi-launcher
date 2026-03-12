<div align="center">

# 🎮 Roblox Multi-Account Launcher

**Launch multiple Roblox accounts simultaneously — no switching, no hassle.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Bloxstrap](https://img.shields.io/badge/Requires-Bloxstrap-7c3aed)](https://github.com/bloxstraplabs/bloxstrap/releases)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)

[**GitHub Repository**](https://github.com/Mandi040Gaming/roblox-multi-launcher) · [**Report a Bug**](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues) · [**Request a Feature**](https://github.com/Mandi040Gaming/roblox-multi-launcher/issues)

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

### Step 3 — Download this tool

**Option A — Download ZIP (recommended):**
1. Click the green **Code** button at the top of [this page](https://github.com/Mandi040Gaming/roblox-multi-launcher)
2. Select **Download ZIP**
3. Extract the ZIP to any folder

**Option B — Clone with Git:**
```bash
git clone https://github.com/Mandi040Gaming/roblox-multi-launcher.git
cd roblox-multi-launcher
```

### Step 4 — Run

Double-click **`start.bat`** — it will automatically install all Python dependencies and launch the tool.

> 💡 On first launch, Windows Defender may show a warning. Click **"More info" → "Run anyway"**. This is normal for unsigned scripts — the full source code is available in `roblox_launcher.py` for review.

---

## 🍪 How to get your `.ROBLOSECURITY` Cookie

The tool uses your browser cookie to authenticate with Roblox. No password is ever stored or transmitted.

### Chrome / Edge / Brave

1. Go to [roblox.com](https://www.roblox.com) and log in with the account you want to add
2. Press **F12** to open DevTools
3. Go to the **Application** tab
4. In the left panel: **Storage → Cookies → https://www.roblox.com**
5. Find the row named **`.ROBLOSECURITY`**
6. Double-click the **Value** cell → **Ctrl+A** → **Ctrl+C**
7. Paste into the Cookie field in the launcher

### Firefox

1. Go to [roblox.com](https://www.roblox.com) and log in
2. Press **F12** → open the **Storage** tab
3. In the left panel: **Cookies → https://www.roblox.com**
4. Click `.ROBLOSECURITY` → copy the value on the right side

### Cookie-Editor Extension (easiest method)

1. Install [Cookie-Editor](https://cookie-editor.com) from the Chrome Web Store or Firefox Add-ons
2. Go to roblox.com while logged in with the desired account
3. Click the Cookie-Editor icon in your browser toolbar
4. Find `.ROBLOSECURITY` → click it → copy the value

> ⚠️ The cookie starts with `_|WARNING:-DO-NOT-SHARE...` — make sure you copy the **entire value** (~600 characters). Cookies expire after approximately 30 days and will need to be refreshed.

---

## 📖 Usage

1. **Add an account** — Click **"➕ Add Account"** in the sidebar, enter a display name and paste the `.ROBLOSECURITY` cookie
2. **Select accounts** — Click on account cards to select them (highlighted in blue)
3. **Launch selected** — Click **"▶ Launch Selected"** in the bottom bar, or double-click a card to launch it immediately
4. **Launch all** — Click **"▶▶ Launch All"** in the sidebar to start every account at once

> Each account starts with an **8-second delay** between instances to ensure clean, isolated cookie injection.

---

## 🗂️ File Structure

```
roblox-multi-launcher/
├── roblox_launcher.py     # Main application
├── start.bat              # Windows launcher — run this!
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore
```

**App data stored in `%LOCALAPPDATA%\RobloxMultiLauncher\`:**
```
RobloxMultiLauncher/
├── accounts.json          # Encrypted account list
├── .key                   # Fernet encryption key (never share or commit this!)
├── profiles/              # Isolated per-account Roblox profile folders
│   └── acc_1/
│       └── LocalAppData/
└── avatars/               # Cached profile picture PNGs
```

---

## 🔧 How It Works

1. **Cookie validation** — When you add an account, the cookie is validated against the Roblox Users API to confirm it is active
2. **Auth Ticket** — Before each launch, a short-lived one-time auth ticket is requested from `auth.roblox.com/v1/authentication-ticket` using a two-step CSRF flow
3. **Isolated profiles** — Each account gets its own `LOCALAPPDATA` environment via per-account profile directories, so Roblox instances never share session state
4. **Mutex bypass** — Roblox uses a Windows named mutex (`ROBLOX_singletonEvent`) to block multiple instances. The launcher claims this mutex first, allowing any number of instances to run simultaneously
5. **Direct launch** — `RobloxPlayerBeta.exe` is started directly with the auth ticket URI, bypassing Bloxstrap's interactive menu entirely

---

## ❓ Troubleshooting

**"RobloxPlayerBeta.exe not found"**
> Launch Roblox at least once via Bloxstrap. The tool searches in `%LOCALAPPDATA%\Bloxstrap\Versions\` and `%LOCALAPPDATA%\Roblox\Versions\`.

**"Auth ticket failed"**
> Run the tool from a terminal (`python roblox_launcher.py`) to see detailed console output. The most common cause is an expired cookie — remove the account and re-add it with a freshly copied cookie.

**Roblox opens but lands on the home screen**
> This is expected — the tool launches Roblox without targeting a specific game. Join any game manually after the client loads.

**All instances log in as the same account**
> Each account card must use its own unique cookie copied from a separate browser session logged in as a different Roblox account.

**Windows Defender / Antivirus warning**
> The tool uses standard Windows APIs (registry access, named mutex via `kernel32.dll`) which can trigger heuristic detection. The full source is in `roblox_launcher.py` — nothing is sent to any server other than Roblox's own official APIs.

---

## ⚖️ Legal & Disclaimer

- This project is **not affiliated with, endorsed by, or connected to Roblox Corporation** in any way
- Use is **at your own risk** — multi-account usage may violate [Roblox's Terms of Service](https://en.help.roblox.com/hc/en-us/articles/115004647846)
- All account data is stored **locally on your machine only** — cookies are never uploaded, logged, or transmitted to any third party
- The author is not responsible for any account actions, bans, or other consequences resulting from use of this tool

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — see the file for details.

---

## 🤝 Contributing

Contributions are welcome! For major changes, please open an issue first.

1. Fork the repository at [github.com/Mandi040Gaming/roblox-multi-launcher](https://github.com/Mandi040Gaming/roblox-multi-launcher)
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

<div align="center">
Made with ❤️ &nbsp;—&nbsp; If you find this useful, consider leaving a ⭐ on <a href="https://github.com/Mandi040Gaming/roblox-multi-launcher">GitHub</a>!
</div>
