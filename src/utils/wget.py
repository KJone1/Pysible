import requests


def wget(url: str, dest: str) -> str or None:
    """Downloads a file from a URL.

    Args:
      url: The URL of the file to download.
      dest: The path where the file should be saved.
    """
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return None
    except Exception as e:
        return str(e)
