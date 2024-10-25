from pathlib import Path
from os import path, getenv

ROOT_PASS: str = getenv("ROOT_PASS")
ROOT_DIR: str = Path(__file__).absolute().parent.parent.parent
HOME_DIR = getenv("HOME")
RESOURCES_DIR: str = path.join(ROOT_DIR, "resources")
TMP_DIR: str = path.join(ROOT_DIR, "tmp")
