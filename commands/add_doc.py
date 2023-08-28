from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
import typer

from models.methods.andoc_repository import path_to_andoc_repository


app = typer.Typer(
    help="📜 Add documentation to the specified file or directory.",
    rich_markup_mode="rich",
    epilog="With ❤️ by @gfranciscoerazom",
)

@app.callback(
    help="📜 Adds documentation to the specified file or directory.",
    epilog="With ❤️ by @gfranciscoerazom",
    invoke_without_command=True,
)
def add_doc(
    path: Annotated[
        Path,
        typer.Argument(
            help="📂 The path to the object to add documentation to.",
            rich_help_panel="Optional Arguments",
            exists=True,
            file_okay=True,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=True
        )
    ],

    line: Annotated[
        Optional[int],
        typer.Argument(
            help="🏷️ The line number to add the documentation to.",
            rich_help_panel="Optional Arguments"
        )
    ] = None,
):
    """
    Creates a documentation for the specified file or directory in the andoc folder.
    If the documentation file does not exist, it is created automatically with the same name as the file or directory with the extension .andoc. This files are going to have the same path as the file or directory they are documenting but inside the andoc folder.
    If the documentation file already exists, the documentation is added in ascending order by line number.
    """
    andoc_folder = path_to_andoc_repository(path) #* Continue here

    doc_file = (andoc_folder / path.name).with_suffix('.andoc')
    print(path)
    print(andoc_folder)
    if doc_file.exists():
        return
    else:
        doc_file.touch()
