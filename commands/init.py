import json
from pathlib import Path
from typing_extensions import Annotated
import typer

from models.methods.andoc_repository import has_an_andoc_repository


app = typer.Typer(
    help="🔥 Init provides a way to initialize an andoc repository.",
    rich_markup_mode="rich",
    epilog="With ❤️ by @gfranciscoerazom",
)


def already_have_a_andoc_repository_validation(ctx: typer.Context, path: Path) -> Path | None:
    """
    Checks if the specified path is an andoc repository.
    """
    if ctx.resilient_parsing:
        return
    if has_an_andoc_repository(path):
        raise typer.BadParameter(f"{path} already have an andoc repository")

    return path


@app.callback(
    help="📂 Initializes an andoc repository",
    epilog="With ❤️ by @gfranciscoerazom",
    invoke_without_command=True,
)
def init(
    path: Annotated[
        Path,
        typer.Argument(
            help="📂 The path where the repository will be created.",
            rich_help_panel="Optional Arguments",
            exists=True,
            dir_okay=True,
            file_okay=False,
            writable=True,
            readable=True,
            resolve_path=True,
            callback=already_have_a_andoc_repository_validation
        )
    ] = Path('.')
):
    """
    Initializes an andoc repository at the specified path.
    """

    # Create the repository
    print(f'Initializing andoc repository at "{path.absolute()}"')
    path = (path / 'andoc')
    path.mkdir()

    path_andoc_bookmarks_json = (path / 'andoc.json')
    path_andoc_bookmarks_json.touch()
    with open(path_andoc_bookmarks_json, 'w') as f:
        json.dump(
            {
                'bookmarks': {}
            },
            f,
            indent=4
        )
