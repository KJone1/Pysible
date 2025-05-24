import sh

from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.utils.log_utils import Logger


@task_plugin(name="Install k0s", section=Sections.SOFTWARE)
def install_k0s() -> None:
    Logger.info("Starting to install k0s...")
    try:
        sh.bash("curl -sSLf https://get.k0s.sh | sudo sh")
        sh.bash("k0s install controller --force --single")
    except sh.ErrorReturnCode as e:
        Logger.failure(f"Failed to install k0s -> {e}")
    except Exception as e:
        Logger.failure(f"Caught unexpected k0s error -> {e}")
