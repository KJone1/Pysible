import pysible.software.containers as containers
import requests
from pysible.utils.log_utils import Logger

version_url = "https://dl.k8s.io/release/stable.txt"
try:
    response = requests.get(version_url)
    response.raise_for_status()
    version = response.text.strip()

    containers.install_kubectl(version)

except requests.exceptions.RequestException as e:
    Logger.failure(f"Error fetching Kubernetes version -> {e}")
except Exception as e:
    Logger.failure(f"Caught unexpected error while installing kubectl -> {e}")
