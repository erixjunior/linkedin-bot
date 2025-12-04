from pathlib import Path
from utils import Utils


class Session:
    """Manager untuk session (cookies) storage."""

    def __init__(self, session_dir: str = None, port: int = 9222):
        """Inisialisasi Session manager."""
        self.session_dir = Path(session_dir or "./sessions")
        self.session_dir.mkdir(exist_ok=True)
        self.session_file = self.session_dir / f"session_{port}.json"

    def save(self, page) -> bool:
        """Simpan cookies dari page ke file."""
        if not page:
            print("❌ Page tidak tersedia")
            return False

        try:
            cookies = page.context.cookies()
            return Utils.write_json(str(self.session_file), cookies)
        except Exception as e:
            print(f"❌ Error saat save session: {e}")
            return False

    def load(self, page) -> bool:
        """Load cookies dari file ke page context."""
        if not page or not Utils.file_exists(str(self.session_file)):
            return False

        try:
            cookies = Utils.read_json(str(self.session_file))
            if cookies:
                page.context.add_cookies(cookies)
                print(f"✅ Session dimuat: {len(cookies)} cookies")
                return True
            return False
        except Exception as e:
            print(f"❌ Error saat load session: {e}")
            return False

    def clear(self) -> bool:
        """Hapus session file."""
        return Utils.delete_file(str(self.session_file))

    def exists(self) -> bool:
        """Cek apakah session file ada."""
        return Utils.file_exists(str(self.session_file))
