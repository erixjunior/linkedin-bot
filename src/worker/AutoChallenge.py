import traceback
from PyQt6.QtCore import QMetaObject, QObject, Qt, pyqtSignal, pyqtSlot
from state import Global
from utils import Utils


class AutoChallengeWorker(QObject):
    """QObject untuk handle checkpoint/challenge verification monitoring."""

    # Signals
    challenge_started = pyqtSignal()
    challenge_completed = pyqtSignal(bool)  # (success)
    status_changed = pyqtSignal(str)  # (status message)

    # ________________________________________________________________________________
    def __init__(self):
        """Inisialisasi AutoChallengeWorker."""
        super().__init__()
        self._browser = None
        self._verified = False
        self._checkpoint_detected = False

        print("✅ AutoChallengeWorker initialized")

    # ________________________________________________________________________________
    @pyqtSlot()
    def on_create(self) -> None:
        """Slot untuk setup setelah browser ready."""
        self._browser = Global.get("browser")
        if self._browser:
            self._browser.url_changed.connect(self._on_url_changed)
            print("✅ AutoChallengeWorker signals connected")

    # ________________________________________________________________________________
    @pyqtSlot(str)
    def _on_url_changed(self, new_url: str) -> None:
        """Handle URL change event."""
        # print(f"🔗 URL changed: {new_url}")
        if "linkedin.com/checkpoint/challenge/" in new_url:
            print("⚠️  Checkpoint detected - waiting for user verification")
            QMetaObject.invokeMethod(self, "on_start", Qt.ConnectionType.QueuedConnection)

    # ________________________________________________________________________________
    @pyqtSlot() # auto click reCAPTCHA triggered by url change
    def on_start(self) -> None:
        """Handle checkpoint verification - auto click reCAPTCHA."""
        self._checkpoint_detected = True
        self.challenge_started.emit()
        print("🤖 Trying to click reCAPTCHA checkbox...")

        try:
            browser = Global.get("browser")
            if not browser:
                print("❌ Browser tidak tersedia")
                return

            page = browser.get_page()
            if not page:
                print("❌ Page tidak tersedia")
                return

            # wait for page load
            print("⏳ Waiting for page load...")
            page.wait_for_load_state("domcontentloaded", timeout=5000)
            print("✅ Page loaded")

            # save page content untuk debug
            html_content = page.content()
            Utils.write_file("output/html/challenge_page.html", html_content)
            print(f"✅ Page content saved")

            # wait for reCAPTCHA element
            print("⏳ Waiting for reCAPTCHA element...")
            page.wait_for_selector("iframe#captcha-internal", timeout=5000)
            print("✅ reCAPTCHA element found")

            # Try multiple selectors untuk reCAPTCHA
            recaptcha_selectors = [
                "iframe#captcha-internal",  # Main captcha iframe
                "iframe[title='reCAPTCHA']",  # reCAPTCHA badge iframe
                "span.recaptcha-checkbox-unchecked",  # Checkbox unchecked
                "span.recaptcha-checkbox",  # Checkbox generic
            ]

            for selector in recaptcha_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        print(f"✅ Found element: {selector}")
                        page.click(selector)
                        print(f"✅ Clicked reCAPTCHA: {selector}")
                        break
                except:
                    continue
            else:
                print("⚠️  reCAPTCHA element not found, waiting for manual verification")

        except Exception as e:
            print(f"❌ Error saat click reCAPTCHA: {e}")

        print("⏳ Waiting for user to complete checkpoint verification...")
        self.status_changed.emit("⏳ Please complete the checkpoint verification in browser")
        self._verified = True
        self.challenge_completed.emit(True)

    def is_verified(self) -> bool:
        """Cek apakah sudah verified dari checkpoint."""
        return self._verified

    def reset(self) -> None:
        """Reset verification state."""
        print("🔄 Reset challenge state")
        self._verified = False
        self._checkpoint_detected = False
