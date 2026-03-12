<div align="center">

# 🎮 Roblox Multi-Account Launcher

**Launch multiple Roblox accounts simultaneously — no switching, no hassle.**

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?logo=windows&logoColor=white)
![Bloxstrap](https://img.shields.io/badge/Requires-Bloxstrap-7c3aed)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## ✨ Features

- 🔀 **True multi-instance** — run 2, 3, 4+ Roblox accounts at the same time
- 🎫 **Auth-Ticket login** — each account logs in cleanly via Roblox's own API, no manual switching
- 🛡️ **Encrypted storage** — cookies are stored locally using Fernet encryption, never sent anywhere
- 🖼️ **Profile avatars** — automatically fetches and displays each account's Roblox headshot
- 🎨 **Clean dark UI** — minimal, fast tkinter interface
- 🔒 **Cookie-only** — no passwords stored, ever

---

## 📋 Requirements

| Requirement | Version | Download |
|-------------|---------|----------|
| **Windows** | 10 or 11 (64-bit) | — |
| **Python** | 3.11 or newer | [python.org](https://www.python.org/downloads/) |
| **Bloxstrap** | Latest | [github.com/bloxstraplabs/bloxstrap](https://github.com/bloxstraplabs/bloxstrap/releases) |

> ⚠️ **Roblox must have been launched at least once via Bloxstrap** before using this tool, so that `RobloxPlayerBeta.exe` is installed.

---

## 🚀 Installation

### Step 1 — Install Python

1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **Check "Add Python to PATH"** — this is required!
4. Click "Install Now"

### Step 2 — Install Bloxstrap & Roblox

1. Download Bloxstrap from [github.com/bloxstraplabs/bloxstrap/releases](https://github.com/bloxstraplabs/bloxstrap/releases)
2. Run `Bloxstrap.exe` and let it install Roblox
3. Launch Roblox at least once to make sure everything is downloaded

### Step 3 — Download this tool

**Option A — Download ZIP:**
1. Click the green **Code** button on this page
2. Select **Download ZIP**
3. Extract the ZIP to a folder of your choice

**Option B — Clone with Git:**
```bash
git clone https://github.com/YOUR_USERNAME/roblox-multi-launcher.git
cd roblox-multi-launcher
```

### Step 4 — Run

Double-click **`start.bat`** — it will automatically install all Python dependencies and launch the tool.

> On first launch, Windows Defender might show a warning. Click **"More info" → "Run anyway"**. This is normal for unsigned scripts.

---

## 🍪 How to get your `.ROBLOSECURITY` Cookie

The tool uses your browser cookie to authenticate — no password is ever stored or transmitted.

### Chrome / Edge / Brave

1. Go to [roblox.com](https://www.roblox.com) and log in with the account you want to add
2. Press **F12** to open DevTools
3. Go to the **Application** tab
4. In the left panel: **Storage → Cookies → https://www.roblox.com**
5. Find the row named **`.ROBLOSECURITY`**
6. Double-click the **Value** column → **Ctrl+A** → **Ctrl+C**
7. Paste it into the launcher

### Firefox

1. Go to [roblox.com](https://www.roblox.com) and log in
2. Press **F12** → **Storage** tab
3. **Cookies → https://www.roblox.com**
4. Click `.ROBLOSECURITY` → copy the value on the right

### Cookie-Editor Extension (easiest)

1. Install [Cookie-Editor](https://cookie-editor.com) from the Chrome Web Store
2. Go to roblox.com while logged in
3. Click the Cookie-Editor icon in your toolbar
4. Find `.ROBLOSECURITY` → copy the value

> ⚠️ The cookie starts with `_|WARNING:-DO-NOT-SHARE...` — make sure you copy the **entire value**. Cookies expire after ~30 days and will need to be refreshed.

---

## 📖 Usage

1. **Add accounts** — Click **"➕ Account hinzufügen"** in the sidebar, enter a display name and paste the cookie
2. **Select accounts** — Click on account cards to select them (highlighted in blue)
3. **Launch** — Click **"▶ Ausgewählte Accounts starten"** or double-click a card to launch immediately
4. **Launch all** — Click **"▶▶ Alle starten"** to launch every account

Each account starts with an **8-second delay** between instances to ensure clean cookie injection.

---

## 🗂️ File Structure

```
roblox-multi-launcher/
├── roblox_launcher.py     # Main application
├── start.bat              # Windows launcher (run this!)
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore
```

**Data stored in `%LOCALAPPDATA%\RobloxMultiLauncher\`:**
```
RobloxMultiLauncher/
├── accounts.json          # Encrypted account data
├── .key                   # Encryption key (never share this!)
├── profiles/              # Per-account Roblox profile folders
│   └── acc_1/
│       └── LocalAppData/
└── avatars/               # Cached profile pictures
```

---

## 🔧 How It Works

1. **Cookie validation** — When you add an account, the cookie is validated against the Roblox API
2. **Auth Ticket** — Before each launch, the tool requests a short-lived auth ticket from `auth.roblox.com/v1/authentication-ticket` using the stored cookie
3. **Isolated profiles** — Each account gets its own `LOCALAPPDATA` folder via environment variables, so Roblox instances don't interfere with each other
4. **Mutex bypass** — Roblox uses a Windows mutex (`ROBLOX_singletonEvent`) to prevent multiple instances. The tool holds this mutex, allowing multiple instances to run simultaneously
5. **Direct launch** — `RobloxPlayerBeta.exe` is launched directly with the auth ticket URI, bypassing Bloxstrap's menu entirely

---

## ❓ Troubleshooting

**"RobloxPlayerBeta.exe nicht gefunden"**
> Launch Roblox once via Bloxstrap to install it. The tool searches in `%LOCALAPPDATA%\Bloxstrap\Versions\`.

**"Auth-Ticket fehlgeschlagen"**
> Your cookie may have expired (they last ~30 days). Remove the account and re-add it with a fresh cookie. Run the tool from a terminal (`python roblox_launcher.py`) to see detailed error output.

**Roblox opens but stays on the home screen**
> This is expected — the tool launches Roblox without a specific game. Join any game manually after launching.

**Windows Defender / Antivirus warning**
> The tool uses Windows APIs (registry, mutex) which can trigger heuristic detection. You can review the full source code in `roblox_launcher.py` — nothing is sent to external servers except Roblox's own API.

**Multiple instances all show the same account**
> Make sure you're using a separate cookie for each account. Each cookie must come from a different Roblox session/browser profile.

---

## ⚖️ Legal & Disclaimer

- This tool is **not affiliated with, endorsed by, or connected to Roblox Corporation** in any way
- Use is **at your own risk** — multi-account usage may violate Roblox's Terms of Service
- All account data is stored **locally on your machine only** — cookies are never uploaded, logged, or shared
- The author is not responsible for any account bans or other consequences resulting from use of this tool

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<div align="center">
Made with ❤️ — Star ⭐ the repo if you find it useful!
</div>
