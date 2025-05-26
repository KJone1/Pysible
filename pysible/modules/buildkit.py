import sh

import pysible.utils.file_utils as files
import pysible.utils.net_utils as net
from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir


@task_plugin(name="Install Buildkit", section=Sections.SOFTWARE)
def install_buildkit() -> None:
    version = net.get_latest_version_from_github(
        repo_owner="moby", repo_name="buildkit"
    )
    url = f"https://github.com/moby/buildkit/releases/download/{version}/buildkit-{version}.linux-amd64.tar.gz"
    tmp_dir_name = "buildkit"
    tmp_dir_path = f"{settings.TMP_DIR}/{tmp_dir_name}"
    buildkitd_dest = "/usr/local/bin/buildkitd"
    buildctl_dest = "/usr/local/bin/buildctl"
    Logger.info(f"Starting to install Buildkit {version}...")
    try:
        create_tmp_dir(name=tmp_dir_name)

        local_tar_path = f"{tmp_dir_path}/buildkit-{version}.tar.gz"
        net.wget(url=url, dest=local_tar_path)

        files.untar(input_tar=local_tar_path, output=tmp_dir_path, strip=True)
        files.copy(source=f"{tmp_dir_path}/buildkitd", dest=buildkitd_dest)
        files.copy(source=f"{tmp_dir_path}/buildctl", dest=buildctl_dest)
        files.set_file_permissions(buildkitd_dest, "555")
        files.set_file_permissions(buildctl_dest, "555")
        _ = files.copy_resource(
            filename="buildkit.service",
            dest="/etc/systemd/system/buildkit.service",
            sudo=True,
        )
        _ = files.copy_resource(
            filename="buildkitd.toml",
            dest="/etc/buildkit/buildkitd.toml",
            sudo=True,
        )
        Logger.success(f"Installed buildkit {version}")

    except sh.ErrorReturnCode as e:
        raise TaskFailedException(task_name=__name__, original_exception=e)
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught unexpected builtkit error",
        )
