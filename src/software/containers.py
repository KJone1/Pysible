import sh

import src.utils.file_utils as files
import src.utils.net_utils as net
from src.config.constants import Consts
from src.utils.log_utils import Logger
from src.utils.misc_utils import create_tmp_dir

logger = Logger()


def install_kubectl() -> None:
    KUBE_VER = _get_kubernetes_version()
    KUBECTL_URL = f"https://dl.k8s.io/release/{KUBE_VER}/bin/linux/amd64/kubectl"
    KUBECTL_DEST = "/usr/local/bin/kubectl"

    try:
        logger.info("Starting to install kubectl...")
        net.wget(url=KUBECTL_URL, dest=KUBECTL_DEST)
    except Exception as e:
        logger.failure(f"Failed to download kubectl -> {e}")
    else:
        files.set_file_permissions(KUBECTL_DEST, "555")
        logger.success(f"Installed kubectl {KUBE_VER}")


def install_nerdctl(version: str = "2.0.0") -> None:
    NERDCTL_URL = f"https://github.com/containerd/nerdctl/releases/download/v{version}/nerdctl-{version}-linux-amd64.tar.gz"
    NERDCTL_DEST = "/usr/local/bin/nerdctl"

    try:
        logger.info("Starting to install nerdctl...")
        create_tmp_dir(name="nerdctl")

        TMP_DIR = f"{Consts.TMP_DIR}/nerdctl"
        LOCAL_TAR = f"{TMP_DIR}/nerd-{version}.tar.gz"
        net.wget(url=NERDCTL_URL, dest=LOCAL_TAR)

        files.untar(input=LOCAL_TAR, output=TMP_DIR, strip=False)
        files.copy_file(source=f"{TMP_DIR}/nerdctl", dest=NERDCTL_DEST)

    except Exception as e:
        logger.failure(f"Failed to download nerdctl -> {e}")
    else:
        try:
            files.copy_resource(
                filename="nerdctl.toml",
                dest="/etc/nerdctl/nerdctl.toml",
                sudo=True,
            )
            files.set_file_permissions(NERDCTL_DEST, "555")
            logger.success(f"Installed nerdctl {version}")
        except (OSError, ValueError) as e:
            logger.failure(f"Failed to set nerdctl permissions -> {e}")
        except (sh.ErrorReturnCode, FileNotFoundError) as e:
            logger.failure(f"Failed to copy nerdctl.toml -> {e}")
        except Exception as e:
            logger.failure(f"Caught general nerdctl error -> {e}")


def install_k0s() -> None:
    pass


def install_k9s(version: str = "v0.32.6") -> None:
    K9S_URL = f"https://github.com/derailed/k9s/releases/download/{version}/k9s_Linux_amd64.tar.gz"
    K9S_DEST = "/usr/local/bin/k9s"

    try:
        logger.info("Starting to install k9s...")
        create_tmp_dir(name="k9s")

        TMP_DIR = f"{Consts.TMP_DIR}/k9s"
        LOCAL_TAR = f"{TMP_DIR}/k9s-{version}.tar.gz"
        net.wget(url=K9S_URL, dest=LOCAL_TAR)

        files.untar(input=LOCAL_TAR, output=TMP_DIR, strip=False)
        files.copy_file(source=f"{TMP_DIR}/k9s", dest=K9S_DEST)

    except Exception as e:
        logger.failure(f"Failed to download k9s -> {e}")
    else:
        try:
            files.set_file_permissions(K9S_DEST, "555")
            logger.success(f"Installed k9s {version}")
        except (OSError, ValueError) as e:
            logger.failure(f"Failed to set k9s permissions -> {e}")
        except Exception as e:
            logger.failure(f"Caught general k9s error -> {e}")


def install_buildkit(version: str = "v0.17.0") -> None:
    URL = f"https://github.com/moby/buildkit/releases/download/{version}/buildkit-{version}.linux-amd64.tar.gz"
    TMP_DIR = f"{Consts.TMP_DIR}/buildkit"
    BUILDKITD_DEST = "/usr/local/bin/buildkitd"
    BUILDCTL_DEST = "/usr/local/bin/buildctl"
    try:
        logger.info("Starting to install Buildkit...")
        create_tmp_dir(name="buildkit")

        LOCAL_TAR = f"{TMP_DIR}/buildkit-{version}.tar.gz"
        net.wget(url=URL, dest=LOCAL_TAR)

        files.untar(input=LOCAL_TAR, output=TMP_DIR, strip=True)
        files.copy_file(source=f"{TMP_DIR}/buildkitd", dest=BUILDKITD_DEST)
        files.copy_file(source=f"{TMP_DIR}/buildctl", dest=BUILDCTL_DEST)

    except Exception as e:
        logger.failure(f"Failed to download Buildkit -> {e}")
    else:
        files.set_file_permissions(BUILDKITD_DEST, "555")
        files.set_file_permissions(BUILDCTL_DEST, "555")
        try:
            files.copy_resource(
                filename="buildkit.service",
                dest="/etc/systemd/system/buildkit.service",
                sudo=True,
            )
            files.copy_resource(
                filename="buildkitd.toml",
                dest="/etc/buildkit/buildkitd.toml",
                sudo=True,
            )
        except Exception as e:
            logger.failure(f"Failed to copy buildkit config files -> {e}")

        logger.success(f"Installed buildkit {version}")


def _get_kubernetes_version() -> str:
    """Fetches the latest stable Kubernetes version."""
    import requests

    url = "https://dl.k8s.io/release/stable.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.failure(f"Error fetching Kubernetes version: {e}")
        return None
    else:
        version = response.text.strip()
        return version
