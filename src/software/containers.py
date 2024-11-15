from src.config.constants import Consts
import src.utils.file_utils as files
import src.utils.net_utils as net
from src.utils.misc_utils import create_tmp_dir

from src.utils.log_utils import Logger

logger = Logger()


def install_kubectl() -> None:
    KUBE_VER = _get_kubernetes_version()
    KUBECTL_URL = f"https://dl.k8s.io/release/{KUBE_VER}/bin/linux/amd64/kubectl"
    KUBECTL_DEST = "/usr/local/bin/kubectl"

    try:
        logger.good("Starting to install kubectl...")
        net.wget(url=KUBECTL_URL, dest=KUBECTL_DEST)
    except Exception as e:
        logger.bad(f"Failed to download kubectl -> {e}")
    else:
        files.set_file_permissions(KUBECTL_DEST, "555")
        logger.good(f"Installed kubectl {KUBE_VER}")


def install_nerdctl() -> None:
    pass


def install_k0s() -> None:
    pass


def install_k9s() -> None:
    pass


def install_buildkit(version: str = "v0.17.0") -> None:
    URL = f"https://github.com/moby/buildkit/releases/download/{version}/buildkit-{version}.linux-amd64.tar.gz"
    TMP_DIR = f"{Consts.TMP_DIR}/buildkit"
    BUILDKITD_DEST = "/usr/local/bin/buildkitd"
    BUILDCTL_DEST = "/usr/local/bin/buildctl"
    try:
        logger.good("Starting to install Buildkit...")
        create_tmp_dir(name="buildkit")

        LOCAL_TAR = f"{TMP_DIR}/{version}.tar.gz"
        net.wget(url=URL, dest=LOCAL_TAR)

        files.untar(input=LOCAL_TAR, output=TMP_DIR, strip=True)
        files.copy_file(source=f"{TMP_DIR}/buildkitd", dest=BUILDKITD_DEST)
        files.copy_file(source=f"{TMP_DIR}/buildctl", dest=BUILDCTL_DEST)

    except Exception as e:
        logger.bad(f"Failed to download Buildkit -> {e}")
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
            logger.bad(f"Failed to copy buildkit config files -> {e}")

        logger.good(f"Installed buildkit {version}")


def _get_kubernetes_version() -> str:
    """Fetches the latest stable Kubernetes version."""
    import requests

    url = "https://dl.k8s.io/release/stable.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Kubernetes version: {e}")
        return None
    else:
        version = response.text.strip()
        return version
