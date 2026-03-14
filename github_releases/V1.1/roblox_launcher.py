#!/usr/bin/env python3
"""
Roblox Multi-Account Launcher  •  v3.0
Cookie-only login  •  Auth-Ticket inject  •  Multi-Instance via Mutex
"""

import os, sys, json, time, shutil, threading, subprocess, io
import winreg, ctypes
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path

# ── Dependency check ──────────────────────────────────────────────────────────
_miss = []
try:    import requests
except: _miss.append("requests")
try:    from cryptography.fernet import Fernet
except: _miss.append("cryptography")
try:    from PIL import Image, ImageTk, ImageDraw
except: _miss.append("Pillow")

if _miss:
    root = tk.Tk(); root.withdraw()
    if messagebox.askyesno("Missing packages",
            f"The following packages are missing:\n  {', '.join(_miss)}\n\nInstall them now?"):
        subprocess.run([sys.executable, "-m", "pip", "install"] + _miss + ["--quiet"])
        messagebox.showinfo("Restart required", "Packages installed! Please restart the program.")
    sys.exit(0)

import requests
from cryptography.fernet import Fernet
from PIL import Image, ImageTk, ImageDraw

# ── Paths ─────────────────────────────────────────────────────────────────────
LOCAL    = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
APP_DIR  = LOCAL / "RobloxMultiLauncher"
ACCS_F   = APP_DIR / "accounts.json"
KEY_F    = APP_DIR / ".key"
PROF_DIR = APP_DIR / "profiles"
AV_DIR   = APP_DIR / "avatars"

for _d in (APP_DIR, PROF_DIR, AV_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ── Encryption ────────────────────────────────────────────────────────────────
def _key():
    if not KEY_F.exists():
        KEY_F.write_bytes(Fernet.generate_key())
    return KEY_F.read_bytes()

def enc(s: str) -> str: return Fernet(_key()).encrypt(s.encode()).decode()
def dec(s: str) -> str: return Fernet(_key()).decrypt(s.encode()).decode()

# ── Account storage ───────────────────────────────────────────────────────────
def load_accs() -> list:
    try:
        return json.loads(ACCS_F.read_text("utf-8")) if ACCS_F.exists() else []
    except:
        return []

def save_accs(accs: list):
    ACCS_F.write_text(json.dumps(accs, indent=2, ensure_ascii=False), "utf-8")

def next_id(accs: list) -> str:
    used = {x["id"] for x in accs}
    i = 1
    while str(i) in used:
        i += 1
    return str(i)

# ── Roblox API ────────────────────────────────────────────────────────────────
def validate_cookie(cookie: str) -> dict | None:
    """Validate a cookie against the Roblox API. Returns {'id': ..., 'name': ...} or None."""
    try:
        r = requests.get(
            "https://users.roblox.com/v1/users/authenticated",
            cookies={".ROBLOSECURITY": cookie},
            timeout=10
        )
        if r.status_code == 200:
            d = r.json()
            return {"id": d["id"], "name": d["name"]}
    except:
        pass
    return None

def get_auth_ticket(cookie: str) -> str | None:
    """
    Fetch a one-time auth ticket from the Roblox API.
    Step 1: POST without CSRF → receive 403 + x-csrf-token header
    Step 2: POST with CSRF token → receive the ticket
    """
    try:
        session = requests.Session()
        session.cookies.set(".ROBLOSECURITY", cookie.strip(), domain=".roblox.com")

        base_headers = {
            "User-Agent":     "Roblox/WinInet",
            "Referer":        "https://www.roblox.com/",
            "Origin":         "https://www.roblox.com",
            "Content-Type":   "application/json",
            "Content-Length": "0",
        }

        # Step 1: get CSRF token
        r1 = session.post(
            "https://auth.roblox.com/v1/authentication-ticket",
            headers=base_headers,
            timeout=15
        )
        print(f"[Auth] Step1 status: {r1.status_code}")

        csrf = r1.headers.get("x-csrf-token") or r1.headers.get("X-CSRF-TOKEN", "")
        if not csrf:
            print(f"[Auth] No CSRF token received. Response: {r1.text[:200]}")
            return None

        print(f"[Auth] CSRF token: {csrf[:20]}...")

        # Step 2: fetch ticket with CSRF token
        r2 = session.post(
            "https://auth.roblox.com/v1/authentication-ticket",
            headers={**base_headers, "x-csrf-token": csrf},
            timeout=15
        )
        print(f"[Auth] Step2 status: {r2.status_code}")

        ticket = r2.headers.get("rbx-authentication-ticket", "")
        if ticket:
            print(f"[Auth] Ticket OK: {ticket[:20]}...")
            return ticket

        print(f"[Auth] No ticket in response. Body: {r2.text[:200]}")
        return None

    except Exception as e:
        print(f"[Auth] Exception: {e}")
        return None

def fetch_avatar(user_id, acc_id):
    """Download and cache the avatar image for an account (cropped to circle)."""
    try:
        url = (
            f"https://thumbnails.roblox.com/v1/users/avatar-headshot"
            f"?userIds={user_id}&size=150x150&format=Png&isCircular=true"
        )
        data    = requests.get(url, timeout=10).json()
        img_url = data["data"][0]["imageUrl"]
        raw     = requests.get(img_url, timeout=10).content
        img     = Image.open(io.BytesIO(raw)).convert("RGBA").resize((80, 80), Image.LANCZOS)
        mask    = Image.new("L", (80, 80), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 79, 79], fill=255)
        img.putalpha(mask)
        img.save(AV_DIR / f"{acc_id}.png", "PNG")
    except:
        pass

def get_avatar_img(acc_id, name: str = "?", size: int = 52):
    """Return a PhotoImage for the account avatar, or a placeholder with the initial."""
    path = AV_DIR / f"{acc_id}.png"
    try:
        if path.exists():
            img = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except:
        pass
    # Fallback: colored circle with first letter
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=(35, 45, 70, 255))
    d.text((size // 2, size // 2), (name[0].upper() if name else "?"),
           fill=(120, 140, 200, 255), anchor="mm")
    return ImageTk.PhotoImage(img)

# ── Roblox EXE finder ─────────────────────────────────────────────────────────
def find_roblox_exe() -> Path | None:
    """Search for RobloxPlayerBeta.exe in known Bloxstrap / Roblox install paths."""
    for base in [LOCAL / "Bloxstrap" / "Versions", LOCAL / "Roblox" / "Versions"]:
        if not base.exists():
            continue
        try:
            for folder in sorted(base.iterdir(), reverse=True):
                exe = folder / "RobloxPlayerBeta.exe"
                if exe.exists():
                    return exe
        except:
            pass
    return None

# ── Registry cookie helpers ───────────────────────────────────────────────────
_REG_PATHS = [
    "SOFTWARE\\Roblox\\RobloxBrowser\\roblox.com",
    "SOFTWARE\\Roblox\\RobloxStudioBrowser\\roblox.com",
]

def write_reg_cookie(cookie: str):
    """Write the cookie to the Windows registry in Roblox's expected format."""
    val = f"SEC::<YES>,EXP::<2099-01-01T00:00:00Z>,COOK::<{cookie}>"
    for path in _REG_PATHS:
        try:
            k = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, ".ROBLOSECURITY", 0, winreg.REG_SZ, val)
            winreg.CloseKey(k)
        except:
            pass

def clear_reg_cookie():
    """Remove the cookie from the registry so stale sessions can't persist."""
    for path in _REG_PATHS:
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(k, ".ROBLOSECURITY")
            winreg.CloseKey(k)
        except:
            pass

# ── Multi-instance mutex ──────────────────────────────────────────────────────
_k32          = ctypes.WinDLL("kernel32", use_last_error=True)
_mutex_handle = None
_mutex_lock   = threading.Lock()

def hold_mutex() -> bool:
    """
    Claim the ROBLOX_singletonEvent mutex so Roblox does not block
    additional instances from starting.
    """
    global _mutex_handle
    with _mutex_lock:
        if _mutex_handle:
            return True
        h = _k32.CreateMutexW(None, True, "ROBLOX_singletonEvent")
        if h:
            _mutex_handle = h
            threading.Thread(target=lambda: time.sleep(9e9), daemon=True).start()
            return True
    return False

# ── Profile cache helpers ─────────────────────────────────────────────────────
def clear_profile_cache(fake_local: Path):
    """Delete cached login files so Roblox picks up the fresh auth ticket."""
    rdir = fake_local / "Roblox"
    ls   = rdir / "LocalStorage"
    if ls.exists():
        for f in ls.iterdir():
            try:
                f.unlink()
            except:
                pass
    for name in ["RobloxCookies.dat", ".ROBLOSECURITY"]:
        fp = rdir / name
        if fp.exists():
            try:
                fp.unlink()
            except:
                pass

# ── Launcher ──────────────────────────────────────────────────────────────────
def launch(acc: dict, status_cb, delay: float = 0):
    """
    Full launch sequence for one account:
    1. Prepare isolated profile directory
    2. Clear old cache
    3. Write registry cookie
    4. Fetch auth ticket
    5. Hold singleton mutex
    6. Start RobloxPlayerBeta.exe directly with the auth ticket URI
    """
    time.sleep(delay)
    aid    = acc["id"]
    cookie = dec(acc["cookie_enc"])

    roblox_exe = find_roblox_exe()
    if not roblox_exe:
        status_cb(aid, "error", "RobloxPlayerBeta.exe not found")
        return

    # Set up isolated profile
    prof       = PROF_DIR / f"acc_{aid}"
    fake_local = prof / "LocalAppData"
    roblox_dir = fake_local / "Roblox"
    blox_dir   = fake_local / "Bloxstrap"

    for d in (roblox_dir / "LocalStorage", blox_dir,
              prof / "AppData" / "Roaming", prof / "Temp"):
        d.mkdir(parents=True, exist_ok=True)

    # Junction-link the Versions folder so Roblox finds its executables
    real_vers = roblox_exe.parent.parent
    fake_vers = roblox_dir / "Versions"
    if not fake_vers.exists():
        try:
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(fake_vers), str(real_vers)],
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except:
            pass

    # Copy Bloxstrap settings (FastFlags / mods) if present
    bs_cfg = LOCAL / "Bloxstrap" / "Settings.json"
    if bs_cfg.exists() and not (blox_dir / "Settings.json").exists():
        try:
            shutil.copy2(bs_cfg, blox_dir / "Settings.json")
        except:
            pass

    # Clear stale cache and write fresh registry cookie
    clear_profile_cache(fake_local)
    clear_reg_cookie()
    write_reg_cookie(cookie)

    # Fetch a one-time auth ticket
    status_cb(aid, "msg", "🎫  Fetching auth ticket...")
    ticket = get_auth_ticket(cookie)

    if not ticket:
        status_cb(aid, "error", "Auth ticket failed — check the console for details")
        return

    # Hold the singleton mutex so multiple instances can run
    hold_mutex()

    # Environment variables for isolated profile.
    # IMPORTANT: TEMP/TMP must stay as the real system temp —
    # Roblox uses it for crash dumps and needs a short, valid path.
    # Only LOCALAPPDATA and APPDATA are redirected to the fake profile.
    real_temp = os.environ.get("TEMP", os.environ.get("TMP", str(Path.home())))
    env = os.environ.copy()
    env["LOCALAPPDATA"] = str(fake_local)
    env["APPDATA"]      = str(prof / "AppData" / "Roaming")
    env["TEMP"]         = real_temp
    env["TMP"]          = real_temp

    # Launch RobloxPlayerBeta.exe directly with the auth ticket
    uri = f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchexp:InApp"
    status_cb(aid, "msg", "🚀  Launching...")
    try:
        proc = subprocess.Popen(
            [str(roblox_exe), uri],
            env=env,
            cwd=str(roblox_exe.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(5)
        clear_reg_cookie()
        status_cb(aid, "running", proc.pid)
    except Exception as e:
        status_cb(aid, "error", str(e))

# ══════════════════════════════════════════════════════════════════════════════
#  Design system
# ══════════════════════════════════════════════════════════════════════════════
C = {
    "bg":      "#0a0e1a",
    "surface": "#111827",
    "card":    "#161d2e",
    "border":  "#1f2d45",
    "accent":  "#3b82f6",
    "accent2": "#6366f1",
    "success": "#10b981",
    "warn":    "#f59e0b",
    "danger":  "#ef4444",
    "text":    "#f8fafc",
    "text2":   "#94a3b8",
    "text3":   "#475569",
    "hover":   "#1e293b",
}

def F(size: int = 10, bold: bool = False) -> tuple:
    return ("Segoe UI", size, "bold" if bold else "normal")

# ══════════════════════════════════════════════════════════════════════════════
#  Cookie Guide dialog
# ══════════════════════════════════════════════════════════════════════════════
class CookieGuide(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("How to get your Cookie")
        self.configure(bg=C["bg"])
        self.geometry("580x620")
        self.resizable(False, True)
        self.grab_set()
        self.transient(parent)
        self._ui()

    def _ui(self):
        # Header
        h = tk.Frame(self, bg=C["accent"], height=48)
        h.pack(fill="x")
        h.pack_propagate(False)
        tk.Label(h, text="🍪  Where do I find my cookie?",
            bg=C["accent"], fg="white", font=F(12, True)
        ).pack(side="left", padx=16, pady=12)

        # Scrollable body
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        cv = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        cv.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(cv, bg=C["bg"])
        cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Enter>", lambda e: cv.bind_all("<MouseWheel>",
            lambda e: cv.yview_scroll(-1 * (e.delta // 120), "units")
            if cv.winfo_exists() else None))
        cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))

        def block(title, icon, steps, note=""):
            f = tk.Frame(inner, bg=C["card"],
                highlightbackground=C["border"], highlightthickness=1)
            f.pack(fill="x", padx=14, pady=6)
            hf = tk.Frame(f, bg=C["hover"])
            hf.pack(fill="x")
            tk.Label(hf, text=f"{icon}  {title}",
                bg=C["hover"], fg=C["accent"], font=F(10, True),
                pady=8, padx=12).pack(anchor="w")
            for i, s in enumerate(steps, 1):
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=10, pady=3)
                tk.Label(row, text=str(i),
                    bg=C["accent2"], fg="white", font=F(8, True),
                    width=2).pack(side="left", padx=(0, 10))
                tk.Label(row, text=s,
                    bg=C["card"], fg=C["text"], font=F(9),
                    wraplength=470, justify="left", anchor="w"
                ).pack(side="left", fill="x")
            if note:
                tk.Label(f, text=f"⚠  {note}",
                    bg=C["card"], fg=C["warn"], font=F(8),
                    wraplength=540, justify="left",
                    padx=12, pady=5).pack(fill="x")

        # Info box
        ib = tk.Frame(inner, bg=C["card"],
            highlightbackground=C["accent2"], highlightthickness=1)
        ib.pack(fill="x", padx=14, pady=(14, 4))
        tk.Label(ib, text="ℹ  What is the .ROBLOSECURITY cookie?",
            bg=C["card"], fg=C["accent"], font=F(10, True),
            padx=12, pady=8).pack(anchor="w")
        tk.Label(ib,
            text=(
                "The cookie is a key Roblox stores in your browser when you are logged in.\n"
                "This tool uses it to request an auth ticket and log you into Roblox.\n"
                "It always starts with:  _|WARNING:-DO-NOT-SHARE-THIS..."
            ),
            bg=C["card"], fg=C["text2"], font=F(9),
            padx=12, pady=10, justify="left").pack(anchor="w")

        block("Chrome / Edge / Brave", "🌐", [
            "Go to roblox.com and log in with the account you want to add",
            "Press F12 to open DevTools → click the 'Application' tab",
            "In the left panel: Storage → Cookies → https://www.roblox.com",
            "Find the row named '.ROBLOSECURITY' → double-click the Value cell",
            "Select all (Ctrl+A) and copy (Ctrl+C)",
            "Paste the value into the Cookie field in the launcher",
        ], note="The cookie is ~600 characters long. Make sure to copy the entire value.")

        block("Firefox", "🦊", [
            "Go to roblox.com and log in → press F12 → open the 'Storage' tab",
            "In the left panel: Cookies → https://www.roblox.com",
            "Click '.ROBLOSECURITY' → the value appears on the right side",
            "Double-click the value → Ctrl+A → Ctrl+C",
        ])

        block("Cookie-Editor Extension (easiest method)", "🔧", [
            "Install 'Cookie-Editor' from the Chrome Web Store",
            "Go to roblox.com and log in with the desired account",
            "Click the Cookie-Editor icon in the browser toolbar",
            "Find '.ROBLOSECURITY' → click it → copy the value",
        ])

        block("Common mistakes", "❌", [
            "Expired cookie: Roblox cookies expire after ~30 days — log in again and copy a fresh one",
            "Incomplete copy: The cookie starts with '_|WARNING:' — ensure you copied everything",
            "Wrong account: Verify that roblox.com shows the correct account before copying",
        ])

        tk.Button(inner, text="✓  Close", command=self.destroy,
            bg=C["accent"], fg="white", font=F(10, True),
            relief="flat", pady=10, cursor="hand2"
        ).pack(fill="x", padx=14, pady=10)

# ══════════════════════════════════════════════════════════════════════════════
#  Add Account dialog (cookie only)
# ══════════════════════════════════════════════════════════════════════════════
class AddDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Account")
        self.configure(bg=C["bg"])
        self.geometry("460x340")
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)
        self.result = None
        self._ui()
        self.wait_window()

    def _ui(self):
        # Header
        h = tk.Frame(self, bg=C["accent2"], height=48)
        h.pack(fill="x")
        h.pack_propagate(False)
        tk.Label(h, text="➕  Add Account",
            bg=C["accent2"], fg="white", font=F(12, True)
        ).pack(side="left", padx=16, pady=12)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # Display name
        tk.Label(body, text="Display name",
            bg=C["bg"], fg=C["text2"], font=F(9)).pack(anchor="w")
        self.e_name = tk.Entry(body,
            bg=C["card"], fg=C["text"], insertbackground=C["accent"],
            font=F(10), relief="flat",
            highlightthickness=1, highlightbackground=C["border"],
            highlightcolor=C["accent"])
        self.e_name.pack(fill="x", ipady=7, pady=(2, 12))

        # Cookie
        tk.Label(body, text=".ROBLOSECURITY Cookie",
            bg=C["bg"], fg=C["text2"], font=F(9)).pack(anchor="w")
        self.e_cookie = tk.Entry(body,
            bg=C["card"], fg=C["text"], insertbackground=C["accent"],
            font=("Consolas", 9), relief="flat",
            highlightthickness=1, highlightbackground=C["border"],
            highlightcolor=C["accent"])
        self.e_cookie.pack(fill="x", ipady=7, pady=(2, 4))

        tk.Button(body, text="❓  Where do I find the cookie?",
            command=lambda: CookieGuide(self),
            bg=C["bg"], fg=C["accent"], font=F(8),
            relief="flat", pady=3, cursor="hand2", anchor="w"
        ).pack(anchor="w", pady=(0, 12))

        # Buttons
        bf = tk.Frame(body, bg=C["bg"])
        bf.pack(fill="x")
        tk.Button(bf, text="Cancel", command=self.destroy,
            bg=C["card"], fg=C["text2"], font=F(9),
            relief="flat", padx=14, pady=7, cursor="hand2"
        ).pack(side="left", padx=(0, 6))
        tk.Button(bf, text="✅  Save", command=self._save,
            bg=C["accent"], fg="white", font=F(10, True),
            relief="flat", padx=14, pady=7, cursor="hand2"
        ).pack(side="left")

    def _save(self):
        name   = self.e_name.get().strip()
        cookie = self.e_cookie.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a display name.", parent=self)
            return
        if len(cookie) < 50:
            messagebox.showerror("Error",
                "Cookie is missing or too short.\nPlease paste the full cookie value.",
                parent=self)
            return
        self.result = {"name": name, "cookie": cookie}
        self.destroy()

# ══════════════════════════════════════════════════════════════════════════════
#  Account card widget
# ══════════════════════════════════════════════════════════════════════════════
class AccountCard(tk.Frame):
    def __init__(self, parent, acc: dict, app):
        super().__init__(parent, bg=C["card"],
            highlightbackground=C["border"], highlightthickness=1,
            cursor="hand2")
        self.acc  = acc
        self.app  = app
        self._sel = False
        self._img = None
        self._build()
        self.bind("<Button-1>",        self._click)
        self.bind("<Double-Button-1>", self._dbl)

    def _build(self):
        # Avatar
        av = tk.Frame(self, bg=C["card"], padx=12, pady=10)
        av.pack(side="left")
        av.bind("<Button-1>",        self._click)
        av.bind("<Double-Button-1>", self._dbl)
        self._av_lbl = tk.Label(av, bg=C["card"])
        self._av_lbl.pack()
        self._av_lbl.bind("<Button-1>",        self._click)
        self._av_lbl.bind("<Double-Button-1>", self._dbl)
        self.reload_avatar()

        # Info
        info = tk.Frame(self, bg=C["card"])
        info.pack(side="left", fill="both", expand=True, pady=10)
        info.bind("<Button-1>",        self._click)
        info.bind("<Double-Button-1>", self._dbl)

        self._name_lbl = tk.Label(info, text=self.acc["name"],
            bg=C["card"], fg=C["text"], font=F(11, True), anchor="w")
        self._name_lbl.pack(anchor="w")
        self._name_lbl.bind("<Button-1>", self._click)

        rname = self.acc.get("roblox_name", "")
        uid   = self.acc.get("roblox_id", "")
        sub   = f"@{rname}  •  ID {uid}" if rname else "Not validated"
        self._sub = tk.Label(info, text=sub,
            bg=C["card"], fg=C["text3"], font=F(8), anchor="w")
        self._sub.pack(anchor="w")
        self._sub.bind("<Button-1>", self._click)

        self._status_lbl = tk.Label(info, text="⬜  Ready",
            bg=C["card"], fg=C["text2"], font=F(8), anchor="w")
        self._status_lbl.pack(anchor="w", pady=(3, 0))
        self._status_lbl.bind("<Button-1>", self._click)

        # Action buttons
        bf = tk.Frame(self, bg=C["card"], padx=8)
        bf.pack(side="right", pady=8)

        def btn(text, cmd, bg=C["border"], fg=C["text2"]):
            tk.Button(bf, text=text, command=cmd,
                bg=bg, fg=fg, font=F(8, True), relief="flat",
                padx=10, pady=4, cursor="hand2",
                activebackground=C["accent"], activeforeground="white"
            ).pack(pady=2, fill="x")

        btn("▶  Launch",    lambda: self.app.launch_one(self.acc), C["accent"], "white")
        btn("✏  Rename",    lambda: self.app.rename_acc(self.acc))
        btn("✕  Delete",    lambda: self.app.delete_acc(self.acc), "#2d1010", C["danger"])

    def reload_avatar(self):
        img = get_avatar_img(self.acc["id"], self.acc.get("name", "?"), 52)
        self._img = img
        self._av_lbl.configure(image=img)

    def set_status(self, text: str, color: str = None):
        self._status_lbl.configure(text=text, fg=color or C["text2"])

    def set_sel(self, v: bool):
        self._sel = v
        col    = C["hover"]  if v else C["card"]
        border = C["accent"] if v else C["border"]
        self.configure(bg=col, highlightbackground=border)
        for w in self.winfo_children():
            try: w.configure(bg=col)
            except: pass
            for ww in w.winfo_children():
                try: ww.configure(bg=col)
                except: pass

    def _click(self, _): self.app.toggle_sel(self.acc["id"])
    def _dbl(self,   _): self.app.launch_one(self.acc)

# ══════════════════════════════════════════════════════════════════════════════
#  Main application
# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Roblox Multi-Account Launcher")
        self.geometry("880x660")
        self.minsize(720, 480)
        self.configure(bg=C["bg"])

        self.accs   = load_accs()
        self._sel   : set[str]             = set()
        self._cards : dict[str, AccountCard] = {}

        self._build()
        self._reload()

    # ── Layout ─────────────────────────────────────────────────────────────────
    def _build(self):
        sidebar = tk.Frame(self, bg=C["surface"], width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._sb = sidebar
        self._build_sidebar()

        tk.Frame(self, bg=C["border"], width=1).pack(side="left", fill="y")

        main = tk.Frame(self, bg=C["bg"])
        main.pack(side="left", fill="both", expand=True)
        self._build_main(main)

    def _build_sidebar(self):
        s = self._sb

        # Logo bar
        logo = tk.Frame(s, bg=C["accent"], height=64)
        logo.pack(fill="x")
        logo.pack_propagate(False)
        tk.Label(logo, text="🎮  Multi Launcher",
            bg=C["accent"], fg="white", font=F(12, True)).pack(expand=True)

        tk.Frame(s, bg=C["border"], height=1).pack(fill="x")

        # System status
        sf = tk.Frame(s, bg=C["surface"])
        sf.pack(fill="x", padx=10, pady=10)
        rpe_ok = find_roblox_exe() is not None

        def status_row(icon, label, ok):
            r = tk.Frame(sf, bg=C["card"],
                highlightbackground=C["border"], highlightthickness=1)
            r.pack(fill="x", pady=2)
            tk.Label(r, text=icon,
                bg=C["card"], fg=C["success"] if ok else C["danger"],
                font=F(10), padx=8, pady=5).pack(side="left")
            tk.Label(r, text=label,
                bg=C["card"], fg=C["text2"], font=F(8)).pack(side="left")

        status_row("●", f"RobloxPlayer {'found' if rpe_ok else 'not found'}", rpe_ok)

        tk.Frame(s, bg=C["border"], height=1).pack(fill="x")

        # Navigation buttons
        def nav(icon, label, cmd):
            f = tk.Frame(s, bg=C["surface"])
            f.pack(fill="x")
            tk.Button(f, text=f"  {icon}   {label}",
                command=cmd,
                bg=C["surface"], fg=C["text"], font=F(9),
                relief="flat", padx=8, pady=9,
                anchor="w", cursor="hand2",
                activebackground=C["hover"], activeforeground=C["text"]
            ).pack(fill="x")

        nav("➕", "Add Account",       self._add)
        nav("▶▶", "Launch All",        self._launch_all)
        nav("▶",  "Launch Selected",   self._launch_sel)
        nav("✕",  "Clear Selection",   self._clear_sel)
        nav("🍪", "Cookie Guide",      lambda: CookieGuide(self))

        tk.Frame(s, bg=C["border"], height=1).pack(fill="x")

        # Stats
        self._stats_lbl = tk.Label(s, text="",
            bg=C["surface"], fg=C["text3"], font=F(8),
            justify="left", padx=14, pady=8)
        self._stats_lbl.pack(anchor="w")

        # Spacer
        tk.Frame(s, bg=C["bg"]).pack(fill="both", expand=True)

        # Multi-instance mutex panel
        mx = tk.Frame(s, bg=C["card"],
            highlightbackground=C["border"], highlightthickness=1)
        mx.pack(fill="x", padx=10, pady=6)
        tk.Label(mx, text="Multi-Instance",
            bg=C["card"], fg=C["text3"], font=F(8, True),
            padx=10, pady=4).pack(anchor="w")
        self._mx_lbl = tk.Label(mx, text="⬜  Not yet active",
            bg=C["card"], fg=C["text3"], font=F(8), padx=10, pady=2)
        self._mx_lbl.pack(anchor="w")
        tk.Button(mx, text="Activate",
            command=self._activate_mutex,
            bg=C["border"], fg=C["accent"], font=F(8, True),
            relief="flat", padx=8, pady=3, cursor="hand2"
        ).pack(fill="x", padx=8, pady=(2, 6))

    def _build_main(self, parent):
        # Top bar
        tb = tk.Frame(parent, bg=C["surface"], height=52)
        tb.pack(fill="x")
        tb.pack_propagate(False)

        tk.Label(tb, text="Accounts",
            bg=C["surface"], fg=C["text"], font=F(14, True)
        ).pack(side="left", padx=20, pady=14)

        # Search box
        self._q = tk.StringVar()
        self._q.trace("w", lambda *_: self._reload())
        se = tk.Entry(tb, textvariable=self._q,
            bg=C["card"], fg=C["text"], insertbackground=C["accent"],
            font=F(10), relief="flat",
            highlightthickness=1, highlightbackground=C["border"],
            highlightcolor=C["accent"], width=20)
        se.pack(side="right", padx=16, ipady=6, pady=11)
        tk.Label(tb, text="🔍",
            bg=C["surface"], fg=C["text2"], font=F(11)).pack(side="right")

        tk.Frame(parent, bg=C["border"], height=1).pack(fill="x")

        # Scrollable account list
        outer = tk.Frame(parent, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        self._cv = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=self._cv.yview)
        self._cv.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._cv.pack(side="left", fill="both", expand=True)
        self._cf = tk.Frame(self._cv, bg=C["bg"])
        self._cw = self._cv.create_window((0, 0), window=self._cf, anchor="nw")
        self._cf.bind("<Configure>",
            lambda e: self._cv.configure(scrollregion=self._cv.bbox("all")))
        self._cv.bind("<Configure>",
            lambda e: self._cv.itemconfig(self._cw, width=e.width))
        self._cv.bind("<Enter>", lambda e: self._cv.bind_all("<MouseWheel>",
            lambda e: self._cv.yview_scroll(-1 * (e.delta // 120), "units")
            if self._cv.winfo_exists() else None))
        self._cv.bind("<Leave>", lambda e: self._cv.unbind_all("<MouseWheel>"))

        # Bottom launch bar
        bot = tk.Frame(parent, bg=C["surface"], pady=10)
        bot.pack(fill="x", side="bottom")
        tk.Button(bot,
            text="▶  Launch Selected  •  Double-click a card to launch immediately",
            command=self._launch_sel,
            bg=C["accent"], fg="white", font=F(10, True),
            relief="flat", pady=10, cursor="hand2",
            activebackground=C["accent2"], activeforeground="white"
        ).pack(fill="x", padx=12)

        # Status bar
        self._stbar = tk.Label(parent, text="Ready",
            bg=C["card"], fg=C["text3"], font=F(8),
            anchor="w", padx=12, pady=4)
        self._stbar.pack(fill="x", side="bottom")

    # ── Account cards ──────────────────────────────────────────────────────────
    def _reload(self):
        for w in self._cf.winfo_children():
            w.destroy()
        self._cards.clear()

        q     = self._q.get().lower() if hasattr(self, "_q") else ""
        shown = [a for a in self.accs
                 if q in a["name"].lower() or q in a.get("roblox_name", "").lower()]

        if not shown:
            tk.Label(self._cf,
                text=("No results." if q else "No accounts yet.\n➕ Add Account"),
                bg=C["bg"], fg=C["text3"], font=F(13), pady=60
            ).pack(expand=True)
        else:
            for acc in shown:
                card = AccountCard(self._cf, acc, self)
                card.pack(fill="x", padx=12, pady=3)
                self._cards[acc["id"]] = card
                if acc["id"] in self._sel:
                    card.set_sel(True)

        n = len(self.accs)
        s = len(self._sel)
        self._stats_lbl.configure(text=f"Accounts:  {n}\nSelected:  {s}")

    def _setstatus(self, text: str, color: str = None):
        self._stbar.configure(text=text, fg=color or C["text3"])

    # ── Selection ──────────────────────────────────────────────────────────────
    def toggle_sel(self, acc_id: str):
        if acc_id in self._sel:
            self._sel.discard(acc_id)
            if acc_id in self._cards:
                self._cards[acc_id].set_sel(False)
        else:
            self._sel.add(acc_id)
            if acc_id in self._cards:
                self._cards[acc_id].set_sel(True)
        n = len(self.accs)
        s = len(self._sel)
        self._stats_lbl.configure(text=f"Accounts:  {n}\nSelected:  {s}")

    def _clear_sel(self):
        for aid in list(self._sel):
            if aid in self._cards:
                self._cards[aid].set_sel(False)
        self._sel.clear()
        self._reload()

    # ── Account operations ─────────────────────────────────────────────────────
    def _add(self):
        dlg = AddDialog(self)
        d   = dlg.result
        if not d:
            return

        cookie = d["cookie"]
        self._setstatus("🔍  Validating cookie...")
        self.update()

        info = validate_cookie(cookie)
        if not info:
            if not messagebox.askyesno("Invalid cookie",
                "The cookie could not be validated.\n"
                "It may have expired or was copied incorrectly.\n\n"
                "Save anyway?"):
                self._setstatus("Cancelled.")
                return

        acc = {
            "id":         next_id(self.accs),
            "name":       d["name"],
            "cookie_enc": enc(cookie),
        }
        if info:
            acc["roblox_id"]   = info["id"]
            acc["roblox_name"] = info["name"]

        self.accs.append(acc)
        save_accs(self.accs)
        self._reload()
        self._setstatus(f"✅  '{d['name']}' added.", C["success"])

        # Load avatar in background
        if info:
            aid = acc["id"]
            def bg():
                fetch_avatar(info["id"], aid)
                self.after(0, lambda: self._cards.get(aid) and
                    self._cards[aid].reload_avatar())
            threading.Thread(target=bg, daemon=True).start()

    def rename_acc(self, acc: dict):
        n = simpledialog.askstring("Rename account", "New display name:",
            parent=self, initialvalue=acc["name"])
        if n and n.strip():
            acc["name"] = n.strip()
            save_accs(self.accs)
            self._reload()

    def delete_acc(self, acc: dict):
        if not messagebox.askyesno("Delete account",
            f"Delete '{acc['name']}' and all associated data?"):
            return
        self.accs = [a for a in self.accs if a["id"] != acc["id"]]
        for p in (PROF_DIR / f"acc_{acc['id']}", AV_DIR / f"{acc['id']}.png"):
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            elif p.exists():
                p.unlink(missing_ok=True)
        self._sel.discard(acc["id"])
        save_accs(self.accs)
        self._reload()

    # ── Mutex ──────────────────────────────────────────────────────────────────
    def _activate_mutex(self):
        if hold_mutex():
            self._mx_lbl.configure(text="✅  Active", fg=C["success"])
            self._setstatus("✅  Multi-instance mutex active.", C["success"])
        else:
            self._mx_lbl.configure(text="❌  Failed", fg=C["danger"])

    # ── Launch callbacks ───────────────────────────────────────────────────────
    def _status_cb(self, acc_id: str, event: str, extra=None):
        def do():
            c = self._cards.get(acc_id)
            if not c:
                return
            if event == "msg":
                c.set_status(extra, C["warn"])
            elif event == "running":
                c.set_status(f"✅  Running  (PID {extra})", C["success"])
                self._setstatus(f"✅  Launched (PID {extra})", C["success"])
                self._mx_lbl.configure(text="✅  Active", fg=C["success"])
            elif event == "error":
                c.set_status(f"❌  {extra}", C["danger"])
                self._setstatus(f"❌  {extra}", C["danger"])
        self.after(0, do)

    def launch_one(self, acc: dict):
        if not find_roblox_exe():
            messagebox.showerror("Not found",
                "RobloxPlayerBeta.exe was not found.\n"
                "Make sure Roblox has been installed via Bloxstrap.")
            return
        if acc["id"] in self._cards:
            self._cards[acc["id"]].set_status("⏳  Starting...", C["warn"])
        threading.Thread(
            target=launch, args=(acc, self._status_cb, 0), daemon=True
        ).start()

    def _launch_sel(self):
        ids = list(self._sel)
        if not ids:
            messagebox.showinfo("No selection",
                "Please select at least one account.\n"
                "Click = select  •  Double-click = launch immediately")
            return
        if not find_roblox_exe():
            messagebox.showerror("Not found", "RobloxPlayerBeta.exe was not found.")
            return
        for i, aid in enumerate(ids):
            acc = next((a for a in self.accs if a["id"] == aid), None)
            if not acc:
                continue
            if aid in self._cards:
                self._cards[aid].set_status(f"⏳  Starting in {i * 8}s...", C["warn"])
            threading.Thread(
                target=launch, args=(acc, self._status_cb, i * 8.0), daemon=True
            ).start()
        self._setstatus(f"🚀  Launching {len(ids)} account(s)...")

    def _launch_all(self):
        if not self.accs:
            messagebox.showinfo("No accounts", "No accounts have been added yet.")
            return
        if not find_roblox_exe():
            messagebox.showerror("Not found", "RobloxPlayerBeta.exe was not found.")
            return
        for i, acc in enumerate(self.accs):
            if acc["id"] in self._cards:
                self._cards[acc["id"]].set_status(f"⏳  Starting in {i * 8}s...", C["warn"])
            threading.Thread(
                target=launch, args=(acc, self._status_cb, i * 8.0), daemon=True
            ).start()
        self._setstatus(f"🚀  Launching all {len(self.accs)} accounts...")

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    App().mainloop()
