import sys
import traceback
from PyQt6.QtCore import QCoreApplication, QMetaObject, QObject, QTimer, Qt, pyqtSlot
from src.browser import Browser
from src.worker.AutoLogin import AutoLoginWorker
from src.worker.AutoChallenge import AutoChallengeWorker
from state import Global
from config import Config


class MainApp(QObject):
    """Main application class untuk LinkedIn Bot."""

    def __init__(self, app: QCoreApplication):
        """Inisialisasi MainApp."""
        super().__init__()
        self.app = app
        self.browser = None
        self.auto_login = None
        self.auto_challenge = None
        self.is_ready = False

    def __enter__(self):
        """Context manager enter."""

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        print("\n🛑 Menutup browser...")
        if self.browser:
            self.browser.disconnect()
            Global.remove("browser")
        print("✅ Selesai!")
        return False

    @pyqtSlot()
    def on_create(self) -> None:
        if self.is_ready:
            return

        """Slot untuk handle creation/initialization."""
        self.browser = Browser(port=Config.BROWSER_PORT, session_dir=Config.SESSION_DIR)
        Global.set("browser", self.browser)

        self.auto_login = AutoLoginWorker(email=Config.LINKEDIN_EMAIL, password=Config.LINKEDIN_PASSWORD)
        Global.set("auto_login", self.auto_login)

        self.auto_challenge = AutoChallengeWorker()
        Global.set("auto_challenge", self.auto_challenge)

        QMetaObject.invokeMethod(self, "on_start", Qt.ConnectionType.QueuedConnection)
        self.is_ready = True

    @pyqtSlot()
    def on_start(self) -> None:
        """Slot untuk handle start/launch aplikasi."""
        print("🚀 Meluncurkan browser...")
        self.browser.launch()
        print("✅ Browser telah diluncurkan")

        # Invoke on_create di workers setelah browser ready
        QMetaObject.invokeMethod(self.auto_login, "on_create", Qt.ConnectionType.DirectConnection)
        QMetaObject.invokeMethod(self.auto_challenge, "on_create", Qt.ConnectionType.DirectConnection)

        print("📍 Navigasi ke LinkedIn login page...")
        page = self.browser.get_page()
        if page:
            page.goto("https://www.linkedin.com/login")

    @pyqtSlot()
    def _on_login_started(self) -> None:
        """Handle login started."""
        print("📍 Login process started")

    @pyqtSlot(bool)
    def _on_login_completed(self, success: bool) -> None:
        """Handle login completed signal."""
        print(f"\n📍 Login completed: {success}")
        if success:
            print("✅ Login successful! Monitoring untuk feed...")
        else:
            print("⚠️  Login tidak berhasil")

    @pyqtSlot(bool)
    def _on_challenge_completed(self, success: bool) -> None:
        """Handle challenge completed signal."""
        print(f"\n📍 Challenge completed: {success}")
        if success:
            print("✅ Challenge verification completed!")
            print("💾 Menyimpan session...")
            self.browser.save_session()
            print("✅ Session tersimpan!")
            self.app.quit()

    @pyqtSlot(str)
    def _on_status_changed(self, status: str) -> None:
        """Handle status change signal."""
        print(f"📊 Status: {status}")

    def run(self) -> None:
        """Jalankan aplikasi utama (entry point)."""
        try:
            QMetaObject.invokeMethod(self, "on_create", Qt.ConnectionType.QueuedConnection)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            traceback.print_exc()
            self.app.quit()


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    with MainApp(app) as mainapp:
        mainapp.run()
        sys.exit(app.exec())
