# services/storage_manager.py
# Simple local storage handler with optional future S3/GCS hooks.

from pathlib import Path
import shutil

class StorageManager:
    def __init__(self, base_dir="data"):
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)

    def save_uploaded_file(self, uploaded_file, dest_name=None):
        dest_name = dest_name or getattr(uploaded_file, "name", "uploaded_file")
        dest = self.base / dest_name
        with open(dest, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(dest)

    def list_files(self):
        return [str(x) for x in self.base.glob("*")]

    def remove(self, filename):
        p = self.base / filename
        if p.exists():
            p.unlink()
            return True
        return False
