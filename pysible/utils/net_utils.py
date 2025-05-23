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
                    f.write(chunk)
    except requests.HTTPError as e:
        raise requests.HTTPError(f"HTTP error occurred: {e}") from e
    except Exception as e:
        raise RuntimeError(f"wget error occurred while downloading {url} : {e}") from e


def git_clone(repo_url, dest) -> None:
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
