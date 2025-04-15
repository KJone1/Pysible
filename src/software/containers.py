import sh

import src.utils.file_utils as files
import src.utils.net_utils as net
from src.config.constants import Consts
from src.utils.log_utils import Logger
from src.utils.misc_utils import create_tmp_dir


def install_kubectl(version: str) -> None:

    kubectl_ver = f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"
    kubectl_dest = "/usr/local/bin/kubectl"

    try:
        net.wget(url=kubectl_ver, dest=kubectl_dest)
        files.set_file_permissions(kubectl_dest, "555")
    except Exception:
        raise


def install_nerdctl(version: str = "2.0.0") -> None:
    nerdctl_url = f"https://github.com/containerd/nerdctl/releases/download/v{version}/nerdctl-{version}-linux-amd64.tar.gz"
    nerdctl_bin_dest = "/usr/local/bin/nerdctl"

    Logger.info("Starting to install nerdctl...")
    try:

        create_tmp_dir(name="nerdctl")

        tmp_dir = f"{Consts.TMP_DIR}/nerdctl"
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


def install_k9s(version: str = "v0.32.6") -> None:
    k9s_url = f"https://github.com/derailed/k9s/releases/download/{version}/k9s_Linux_amd64.tar.gz"
    k9s_dest = "/usr/local/bin/k9s"
    Logger.info("Starting to install k9s...")

    try:
        create_tmp_dir(name="k9s")

        tmp_dir = f"{Consts.TMP_DIR}/k9s"
        local_tar_name = f"{tmp_dir}/k9s-{version}.tar.gz"
        net.wget(url=k9s_url, dest=local_tar_name)

        files.untar(input=local_tar_name, output=tmp_dir, strip=False)
        files.copy(source=f"{tmp_dir}/k9s", dest=k9s_dest)
        files.set_file_permissions(k9s_dest, "555")
        Logger.success(f"Installed k9s {version}")

    except (OSError, ValueError) as e:
        Logger.failure(f"Failed to set k9s permissions -> {e}")
    except Exception as e:
        Logger.failure(f"Caught unexpected k9s error -> {e}")


def install_buildkit(version: str = "v0.17.0") -> None:
    URL = f"https://github.com/moby/buildkit/releases/download/{version}/buildkit-{version}.linux-amd64.tar.gz"
    TMP_DIR = f"{Consts.TMP_DIR}/buildkit"
    BUILDKITD_DEST = "/usr/local/bin/buildkitd"
    BUILDCTL_DEST = "/usr/local/bin/buildctl"
    try:
        Logger.info("Starting to install Buildkit...")
        create_tmp_dir(name="buildkit")

        LOCAL_TAR = f"{TMP_DIR}/buildkit-{version}.tar.gz"
        net.wget(url=URL, dest=LOCAL_TAR)

        files.untar(input=LOCAL_TAR, output=TMP_DIR, strip=True)
        files.copy(source=f"{TMP_DIR}/buildkitd", dest=BUILDKITD_DEST)
        files.copy(source=f"{TMP_DIR}/buildctl", dest=BUILDCTL_DEST)

    except Exception as e:
        Logger.failure(f"Failed to download Buildkit -> {e}")
    else:
        files.set_file_permissions(BUILDKITD_DEST, "555")
        files.set_file_permissions(BUILDCTL_DEST, "555")
        try:
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
        except Exception as e:
            Logger.failure(f"Failed to copy buildkit config files -> {e}")

        Logger.success(f"Installed buildkit {version}")
