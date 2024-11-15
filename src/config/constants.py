from pathlib import Path

from dataclasses import dataclass
import os
import src.config.config as config


@dataclass(frozen=True)
class Consts:
    ROOT_PASS: str = config.load_env("ROOT_PASS")
    ROOT_DIR: Path = Path(__file__).absolute().parent.parent.parent
    HOME_DIR: str = os.getenv("HOME")
    RESOURCES_DIR: Path = ROOT_DIR / "resources"
    TMP_DIR: Path = ROOT_DIR / "tmp"
    
