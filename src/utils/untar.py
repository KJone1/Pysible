import tarfile
from os import path, sep


def untar(input: str, output: str, strip: bool = False) -> str or None:
    try:
        with tarfile.open(input, "r:gz") as tar:
            if strip:
                # --strip=1
                for member in tar.getmembers():
                    stripped_name = path.relpath(member.name, member.name.split(sep)[0])
                    member.name = stripped_name
                    tar.extract(member, output)
            else:
                tar.extractall(output)
            return None

    except Exception as e:
        return str(e)
