import sh

from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.file_utils import copy_resource
from pysible.utils.log_utils import Logger


@task_plugin(name="Setup sudoers file", section=Sections.SYSTEM)
def setup_sudoers():
    sudoers_file_name = f"{settings.RESOURCES_DIR}/kj"
    sudoers_path = "/etc/sudoers.d/kj"
    try:
        sh.visudo("-c", "-f", sudoers_file_name)
        _ = copy_resource(filename=sudoers_file_name, dest=sudoers_path, sudo=True)
        Logger.info(f"Copied {sudoers_file_name} to {sudoers_path}")
    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error validating sudoers file",
        )
    except FileNotFoundError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Sudoers file not found",
        )
