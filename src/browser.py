from pathlib import Path
from playwright.sync_api import sync_playwright
from PyQt6.QtCore import QObject, pyqtSignal
from src.session import Session


class Browser(QObject):
    """Manager untuk handle browser connection dan pages via CDP (Qt-based)."""

    # Signals
    url_changed = pyqtSignal(str)  # (new_url)
    page_loaded = pyqtSignal(object)  # (page object)
    page_navigated = pyqtSignal(str)  # (new_url)

    # ________________________________________________________________________________
    def __init__(self, port: int = 9222, session_dir: str = None):
        """Inisialisasi Browser dengan port CDP dan session storage."""
        super().__init__()
        self.port = port
        self.browser = None
        self.playwright = None
        self._page = None
        self.session = Session(session_dir=session_dir, port=port)

    # ________________________________________________________________________________
    def _get_stealth_script(self):
        """Dapatkan stealth script dari file."""
        script_path = Path(__file__).parent / "script" / "stealth.js"
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠️  Stealth script tidak ditemukan di {script_path}")
            return ""

    # ________________________________________________________________________________
    def launch(self):
        """Launch browser dengan Playwright dan CDP, buka DevTools."""
        print(f"🚀 Meluncurkan Chrome...")

        self.playwright = sync_playwright().start()

        # Launch browser dengan CDP port dan anti-detection args
        self.browser = self.playwright.chromium.launch(
            args=[
                f"--remote-debugging-port={self.port}",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-popup-blocking",
                "--disable-extensions",
                "--disable-web-resources",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                "--allow-running-insecure-content",
                "--disable-web-security",
                "--disable-features=CrossOriginOpenerPolicy,CrossOriginEmbedderPolicy",
            ],
            headless=False,
        )

        print(f"✅ Chrome berhasil diluncurkan")
        print("📍 Untuk membuka DevTools: tekan F12 di browser window")

        return self.browser

    # ________________________________________________________________________________
    def get_page(self):
        """Dapatkan page dari browser dengan stealth injection dan event listeners."""
        if not self.browser:
            print("❌ Browser tidak tersedia")
            return None

        if self._page:
            return self._page

        # Buka context dengan desktop emulation (less strict CORS untuk reCAPTCHA)
        context = self.browser.new_context()
        self._page = context.new_page()

        # Inject stealth script
        self._page.add_init_script(self._get_stealth_script())

        # Setup page event listeners untuk emit url_changed signal
        self._page.on("framenavigated", lambda frame: self.url_changed.emit(frame.url))
        # Setup page load listener untuk emit page_loaded signal
        self._page.on("load", lambda: self.page_loaded.emit(self._page))
        print("✅ Page event listeners setup")

        return self._page

    # ________________________________________________________________________________
    def get_url(self) -> str:
        """Slot untuk get URL dari page (bisa di-invoke dari thread lain)."""
        if not self._page:
            return ""
        try:
            return self._page.url
        except Exception as e:
            print(f"❌ Error saat get_url: {e}")
            return ""

    # ________________________________________________________________________________
    def save_session(self) -> bool:
        """Simpan session (cookies) ke file."""
        pages = self.browser.pages if self.browser else []
        if not pages:
            print("⚠️  Tidak ada pages untuk save session")
            return False

        return self.session.save(pages[0])

    # ________________________________________________________________________________
    def load_session(self) -> bool:
        """Load cookies dari file ke browser."""
        if not self.browser or not self.session.exists():
            return False

        pages = self.browser.pages
        if not pages:
            print("⚠️  Tidak ada pages untuk load cookies")
            return False

        return self.session.load(pages[0])

    # ________________________________________________________________________________
    def clear_session(self) -> bool:
        """Hapus session file."""
        return self.session.clear()

    # ________________________________________________________________________________
    def disconnect(self):
        """Putuskan koneksi dan close browser."""
        self._page = None

        if self.browser:
            self.browser.close()
            print("✅ Browser ditutup")

        if self.playwright:
            self.playwright.stop()

    # ________________________________________________________________________________
    def __enter__(self):
        """Context manager: enter."""
        self.launch()
        return self

    # ________________________________________________________________________________
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: exit."""
        self.disconnect()
