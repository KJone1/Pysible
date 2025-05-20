from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    ROOT_PASS: str
    HOME_DIR: Path = Path.home()
    RESOURCES_DIR_NAME: str = "resources"
    TMP_DIR_NAME: str = "tmp"

    @property
    def ROOT_DIR(self) -> Path:
        return Path(__file__).absolute().parent.parent.parent

    @property
    def RESOURCES_DIR(self) -> Path:
        return self.ROOT_DIR / self.RESOURCES_DIR_NAME

    @property
    def TMP_DIR(self) -> Path:
        return self.ROOT_DIR / self.TMP_DIR_NAME

settings = AppSettings()
