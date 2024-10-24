import requests
from sh import git, ErrorReturnCode
from os import makedirs


def wget(url: str, dest: str) -> None:
    """Downloads a file from a URL.

    Args:
      url: The URL of the file to download.
      dest: The path where the file should be saved.
    Returns:
      None
    """
    try:
        if not url.startswith("http"):
            raise ValueError("Invalid URL format.")

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.HTTPError as e:
        raise requests.HTTPError(f"HTTP error occurred: {e}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e


def git_clone(repo_url, dest) -> None:
    """Clone a Git repository

    Args:
      repo_url: The URL of the Git repository.
      dest: The local directory where the repository should be cloned.
    """
    try:
        makedirs(dest)
        git.clone(repo_url, dest)
    except FileExistsError:
        git.pull(_cwd=dest)
    except ErrorReturnCode as e:
        raise e from e
