import time
import traceback
from PyQt6.QtCore import QMetaObject, QObject, QThread, Qt, QTimer, pyqtSignal, pyqtSlot
from config import Config
from state import Global
from utils import Utils


class AutoLoginWorker(QObject):
    """QObject untuk handle auto-login dengan URL monitoring."""

    # Signals
    login_started = pyqtSignal()
    login_completed = pyqtSignal(bool)  # (success)
    status_changed = pyqtSignal(str)  # (status message)

    # ________________________________________________________________________________
    def __init__(self, email: str, password: str):
        """Inisialisasi AutoLoginWorker."""
        super().__init__()
        self.email = email
        self.password = password
        self._logged_in = False
        self._browser = None

        print("✅ AutoLoginWorker initialized")

    # ________________________________________________________________________________
    @pyqtSlot()
    def on_create(self) -> None:
        """Slot untuk setup setelah browser ready."""
        self._browser = Global.get("browser")
        if self._browser:
            self._browser.url_changed.connect(self._on_url_changed)
            print("✅ AutoLoginWorker signals connected")

    # ________________________________________________________________________________
    @pyqtSlot(str)
    def _on_url_changed(self, new_url: str) -> None:
        """Handle URL change event."""
        # print(f"🔗 URL changed: {new_url}")
        if "linkedin.com/login" in new_url:
            print("📍 Detected LinkedIn login page - trigger login")
            QMetaObject.invokeMethod(self, "on_start", Qt.ConnectionType.QueuedConnection)

    # ________________________________________________________________________________
    @pyqtSlot()  # auto login triggered by url change
    def on_start(self) -> None:
        """Handle login automation."""
        try:
            if not self._browser:
                print("❌ Browser tidak tersedia")
                return

            page = self._browser.get_page()
            if not page:
                print("❌ Page tidak tersedia")
                return

            print("✅ Page berhasil didapat")

            # Wait untuk page fully loaded
            print("⏳ Waiting for page load...")
            try:
                page.wait_for_load_state("domcontentloaded", timeout=5000)
                print("✅ Page DOM loaded")
            except:
                print("⚠️  Page load timeout, continue anyway")

            # save page content untuk debug
            html_content = page.content()
            Utils.write_file("output/html/login_page.html", html_content)
            print(f"✅ Page content saved")

            # Wait untuk form login
            print("⏳ Waiting for login form...")
            try:
                page.wait_for_selector("input[name='session_key']", timeout=3000)
                print("✅ Form login ditemukan")
            except:
                print("⚠️  Form not found, trying query selector...")
                form = page.query_selector("input[name='session_key']")
                if not form:
                    print("❌ Form login tidak ditemukan")
                    self.status_changed.emit("❌ Form login tidak ditemukan")
                    return

            # Isi form
            print(f"✍️  Memasukkan email...")
            page.fill("input[name='session_key']", self.email)

            print(f"✍️  Memasukkan password...")
            page.fill("input[name='session_password']", self.password)

            # Check if checkpoint/captcha page
            if "checkpoint" in page.url:
                print("⚠️  Checkpoint/CAPTCHA page detected - manual verification needed")
                self.status_changed.emit("⚠️  Checkpoint/CAPTCHA detected - please solve manually in browser")
                return

            # Submit
            print(f"🔐 Klik sign in...")
            page.click("button[type='submit']")

            print("✅ Form submitted")
            self.status_changed.emit("✅ Form submitted, waiting for verification")
            self._logged_in = True
            self.login_completed.emit(True)

        except Exception as e:
            print(f"❌ Error di _start_login: {e}")
            self.status_changed.emit(f"❌ Error: {e}")
            traceback.print_exc()

    # ________________________________________________________________________________
    def is_logged_in(self) -> bool:
        """Cek apakah sudah login ke LinkedIn."""
        return self._logged_in
