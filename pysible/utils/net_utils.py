from os import makedirs

import requests
import sh


def wget(url: str, dest: str) -> None:
    """Downloads a file from a URL.

    Args:
      url: The URL of the file to download.
      dest: The path where the file should be saved.
    """
    try:
        if not url.startswith("http"):
            raise ValueError("Invalid URL format.")

        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    _ = f.write(chunk)
    except requests.HTTPError as e:
        raise requests.HTTPError(f"HTTP error occurred: {e}") from e
    except Exception as e:
        raise RuntimeError(f"wget error occurred while downloading {url} : {e}") from e


def git_clone(repo_url: str, dest: str) -> None:
    """Clone a Git repository

    Args:
      repo_url: The URL of the Git repository.
      dest: The local directory where the repository should be cloned.
    """
    try:
        makedirs(dest)
        sh.contrib.git.clone(repo_url, dest)
    except FileExistsError:
        sh.contrib.git.pull(_cwd=dest)

def get_latest_version_from_github(repo_owner:str, repo_name:str):
    """
    Fetches the latest release version (tag name) for a given GitHub repository.

    Args:
        repo_owner (str): The owner of the repository (e.g., 'derailed').
        repo_name (str): The name of the repository (e.g., 'k9s').

    Returns:
        str: The tag name of the latest release, or None if an error occurs.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    response.raise_for_status()
    release_info = response.json()
    return release_info.get("tag_name")
