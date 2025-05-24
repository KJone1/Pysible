import pysible.utils.file_utils as files
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.utils.log_utils import Logger


@task_plugin(name="Setup Moonlander keyboard", section=Sections.SYSTEM)
def setup_moonlander() -> None:
    udev_rules = "50-zsa.rules"
    rules_dir = "/etc/udev/rules.d/"
    try:
        _ = files.copy_resource(filename=udev_rules, dest=rules_dir)
        Logger.success(f"Copied {udev_rules} to {rules_dir}")
    except Exception as e:
        Logger.failure(f"Failed to copy {udev_rules} -> {e}")
