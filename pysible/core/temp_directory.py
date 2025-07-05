from pathlib import Path
import shutil
import os
from types import TracebackType
from pysible.config.settings import settings
from pysible.utils.log_utils import Logger


class TempDirectory:
    def __init__(self, name: str):
        self.name: str = name
        self.path: Path = settings.TMP_DIR / name

    def __enter__(self):
        self.path.mkdir(parents=True, exist_ok=True)
        return str(self.path)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:

        if os.path.exists(settings.TMP_DIR):
            Logger.info(f"Removing temp dir: {self.path}")
            shutil.rmtree(self.path, ignore_errors=True)

        return False
