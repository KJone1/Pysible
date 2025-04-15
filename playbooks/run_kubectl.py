import src.software.containers as containers
import requests
from src.utils.log_utils import Logger

version_url = "https://dl.k8s.io/release/stable.txt"
try:
    response = requests.get(version_url)
    response.raise_for_status()
    version = response.text.strip()

    Logger.info(f"Starting to install kubectl {version}")

    containers.install_kubectl(version)

    Logger.success(f"Installed kubectl {version}")

except requests.exceptions.RequestException as e:
    Logger.failure(f"Error fetching Kubernetes version -> {e}")
except Exception as e:
    Logger.failure(f"Caught unexpected error while intalling kubectl -> {e}")
