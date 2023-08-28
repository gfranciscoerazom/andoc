from pathlib import Path


def path_to_andoc_repository(path: Path) -> Path:
    """
    Returns the path to the andoc folder in the specified path or its parent directories.
    """
    path = path.resolve()
    original_path = path

    while True:
        if has_an_andoc_repository(path):
            return path / 'andoc'
        elif path.parent == path:
            raise FileNotFoundError(f"Invalid path: {original_path} does not have an andoc repository in its parent directories")
        else:
            path = path.parent


def has_an_andoc_repository(path: Path) -> bool:
    """
    Checks if the specified path has an andoc repository.
    """
    return (path / 'andoc').is_dir()


def a_parent_has_an_andoc_repository(path: Path) -> bool:
    """
    Checks if the specified path is inside an andoc repository.
    """
    path = path.resolve()
    while True:
        if has_an_andoc_repository(path):
            return True
        elif path.parent == path:
            return False
        else:
            path = path.parent
