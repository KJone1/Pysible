from loguru import logger

import src.utils.file_utils as files

import src.utils.net_utils as net


def install_kubectl() -> None:
    KUBE_VER = _get_kubernetes_version()
    KUBECTL_URL = f"https://dl.k8s.io/release/{KUBE_VER}/bin/linux/amd64/kubectl"
    KUBECTL_DEST = "/usr/local/bin/kubectl"

    try:
        net.wget(url=KUBECTL_URL, dest=KUBECTL_DEST)
    except Exception as e:
        logger.error(f"Failed to download kubectl with error -> {e}")
    else:
        files.set_file_permissions(KUBECTL_DEST, "555")
        logger.into(f"Installed kubectl {KUBE_VER}")


def install_nerdctl() -> None:
    pass


def install_k0s() -> None:
    pass


def install_k9s() -> None:
    pass


def install_buildkit() -> None:
    pass


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
