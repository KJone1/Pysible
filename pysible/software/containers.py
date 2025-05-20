import sh
import pysible.utils.file_utils as files
import pysible.utils.net_utils as net
import pysible.utils.package_utils as pkg
from pysible.config.settings import settings
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir


def install_kubectl(version: str) -> None:

    kubectl_ver = f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"
    kubectl_dest = "/usr/local/bin/kubectl"

    Logger.info(f"Starting to install kubectl {version}")
    try:
        net.wget(url=kubectl_ver, dest=kubectl_dest)
        files.set_file_permissions(kubectl_dest, "555")
        Logger.success(f"Installed kubectl {version}")
    except Exception:
        raise


def install_nerdctl(version: str = "2.0.0") -> None:
    nerdctl_url = f"https://github.com/containerd/nerdctl/releases/download/v{version}/nerdctl-{version}-linux-amd64.tar.gz"
    nerdctl_bin_dest = "/usr/local/bin/nerdctl"

    Logger.info("Starting to install nerdctl...")
    try:

        create_tmp_dir(name="nerdctl")

        tmp_dir = f"{settings.TMP_DIR}/nerdctl"
        local_tar_name = f"{tmp_dir}/nerd-{version}.tar.gz"
        net.wget(url=nerdctl_url, dest=local_tar_name)

        files.untar(input=local_tar_name, output=tmp_dir, strip=False)
        files.copy(source=f"{tmp_dir}/nerdctl", dest=nerdctl_bin_dest)
        _ = files.copy_resource(
            filename="nerdctl.toml",
            dest="/etc/nerdctl/nerdctl.toml",
            sudo=True,
        )
        files.set_file_permissions(nerdctl_bin_dest, "555")
        Logger.success(f"Installed nerdctl {version}")
    except (OSError, ValueError) as e:
        Logger.failure(f"Failed to set nerdctl permissions -> {e}")
    except (sh.ErrorReturnCode, FileNotFoundError) as e:
        Logger.failure(f"Failed to copy nerdctl.toml -> {e}")
    except Exception as e:
        Logger.failure(f"caught unexpected nerdctl error -> {e}")


def install_k0s() -> None:
    Logger.info("Starting to install k0s...")
    try:
        sh.bash("curl -sSLf https://get.k0s.sh | sudo sh")
        sh.bash("k0s install controller --force --single")
    except sh.ErrorReturnCode as e:
        Logger.failure(f"Failed to install k0s -> {e}")
    except Exception as e:
        Logger.failure(f"Caught unexpected k0s error -> {e}")


def install_k9s(version: str) -> None:
    k9s_url = f"https://github.com/derailed/k9s/releases/download/{version}/k9s_Linux_amd64.rpm"
    k9s_tmp_dir_name = "k9s"
    k9s_tmp_dir_path = f"{settings.TMP_DIR}/{k9s_tmp_dir_name}"

    Logger.info(f"Starting to install k9s {version}...")
    try:
        create_tmp_dir(name=k9s_tmp_dir_name)
        local_rpm_name = f"{k9s_tmp_dir_path}/k9s-{version}.rpm"
        net.wget(url=k9s_url, dest=local_rpm_name)
        _ = pkg.install_package(local_rpm_name)
        Logger.success(f"Installed k9s {version}")

    except Exception:
        raise


def install_buildkit(version: str) -> None:
    url = f"https://github.com/moby/buildkit/releases/download/{version}/buildkit-{version}.linux-amd64.tar.gz"
    tmp_dir_name = "buildkit"
    tmp_dir_path = f"{settings.TMP_DIR}/{tmp_dir_name}"
    buildkitd_dest = "/usr/local/bin/buildkitd"
    buildctl_dest = "/usr/local/bin/buildctl"
    Logger.info("Starting to install Buildkit...")
    try:
        create_tmp_dir(name=tmp_dir_name)

        local_tar_path = f"{tmp_dir_path}/buildkit-{version}.tar.gz"
        net.wget(url=url, dest=local_tar_path)

        files.untar(input=local_tar_path, output=tmp_dir_path, strip=True)
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

    except Exception:
        raise
