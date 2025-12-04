import json
from pathlib import Path
from typing import Any, Optional, Callable
from PyQt6.QtCore import QObject, QMetaObject, Qt, QEventLoop, pyqtSignal, pyqtSlot


class InvokeHelper(QObject):
    """Helper class untuk thread-safe invoke dengan Qt signals/slots."""

    # Signal untuk trigger invoke
    invoke_requested = pyqtSignal()

    def __init__(self, func: Callable, result_holder: list, loop: QEventLoop):
        """Inisialisasi InvokeHelper dengan function, result, dan loop."""
        super().__init__()
        self.func = func
        self.result = result_holder
        self.loop = loop
        # Connect signal ke slot
        self.invoke_requested.connect(self.on_invoke)

    @pyqtSlot()
    def on_invoke(self) -> None:
        """Slot untuk invoke function dengan exception handling."""
        try:
            self.result[0] = self.func()
        except Exception as e:
            print(f"❌ InvokeHelper: Exception during invoke: {e}")
        finally:
            # Quit loop
            self.loop.quit()


class Utils:
    """Static class untuk utility functions."""

    @staticmethod
    def safe_invoke(
        target: QObject,
        func: Callable,
        connection_type=Qt.ConnectionType.QueuedConnection,
    ) -> Any:
        """Invoke function pada target QObject dengan thread-safe execution."""
        if not target:
            print("❌ Target object is null in safe_invoke")
            return None

        if not func:
            print("❌ Function is null in safe_invoke")
            return None

        result = [None]
        loop = QEventLoop()

        try:
            # Create helper dengan function, result, dan loop
            helper = InvokeHelper(func, result, loop)

            # Connect signal dengan connection type
            helper.invoke_requested.connect(helper.on_invoke, connection_type)

            # Emit signal
            helper.invoke_requested.emit()

            # Execute event loop (blocking sampai loop.quit() di-call)
            loop.exec()

        except Exception as e:
            print(f"❌ safe_invoke: Error during invocation: {e}")

        return result[0]

    @staticmethod
    def read_file(file_path: str) -> str:
        """Baca file text dan return contents."""
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"⚠️  File tidak ditemukan: {file_path}")
                return ""

            with open(path, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            print(f"❌ Error saat read file: {e}")
            return ""

    @staticmethod
    def write_file(file_path: str, content: str) -> bool:
        """Tulis content ke file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"✅ File ditulis: {file_path}")
            return True

        except Exception as e:
            print(f"❌ Error saat write file: {e}")
            return False

    @staticmethod
    def read_json(file_path: str) -> Optional[Any]:
        """Baca file JSON dan return parsed object."""
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"⚠️  File JSON tidak ditemukan: {file_path}")
                return None

            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"❌ Error saat read JSON: {e}")
            return None

    @staticmethod
    def write_json(file_path: str, data: Any, indent: int = 2) -> bool:
        """Tulis data ke file JSON."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent)

            print(f"✅ JSON file ditulis: {file_path}")
            return True

        except Exception as e:
            print(f"❌ Error saat write JSON: {e}")
            return False

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Cek apakah file ada."""
        return Path(file_path).exists()

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Hapus file."""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                print(f"✅ File dihapus: {file_path}")
                return True
            else:
                print(f"⚠️  File tidak ditemukan: {file_path}")
                return False

        except Exception as e:
            print(f"❌ Error saat delete file: {e}")
            return False
