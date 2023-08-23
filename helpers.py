from pathlib import Path

def path_to_andoc_folder(path: Path) -> Path:
    """
    Returns the path to the andoc folder in the specified path or its parent directories.
    """

    if not path.exists():
        raise Exception(f"Invalid path: {path} does not exist")

    path = path.resolve()
    while True:
        if (path / 'andoc').exists():
            return path / 'andoc'
        elif path.parent == path:
            raise Exception(f"Invalid path: {path} is not an andoc repository")
        else:
            path = path.parent
