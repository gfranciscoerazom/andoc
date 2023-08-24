from typing import Optional
from typing_extensions import Annotated
from rich import print
from rich.console import Console
from helpers import path_to_andoc_folder
from pathlib import Path
import typer
import os

app = typer.Typer()

err_console = Console(stderr=True)
printerr = err_console.print


@app.command()
def init(
    path: Annotated[
        str,
        typer.Argument(
            help="(str) 📂 The path where the repository will be created.",
            rich_help_panel="Optional Arguments"
        ) # type: ignore
    ] = '.',
    add_to_gitignore: Annotated[
        bool,
        typer.Option(
            help="(bool) Whether to add the andoc directory to the .gitignore file.",
        ) # type: ignore
    ] = False
):
    """
    Initializes an andoc repository at the specified path.
    """
    # Verify that the path exists, if not exit
    if not os.path.exists(path):
        printerr(f"[red]Invalid path:[/red] {path} does [bold underline]not exist[/bold underline]") 
        raise typer.Exit(code=1)

    # Verify that the path is valid, if not exit
    if not os.path.isdir(path):
        printerr(f"[red]Invalid path:[/red] {path} is [bold underline]not a directory[/bold underline]") 
        raise typer.Exit(code=1)
    
    # Check if the path is already an andoc repository, if so exit
    if os.path.isdir(os.path.join(path, 'andoc')):
        printerr(f"[red]Invalid path:[/red] {path} is [bold underline]already an andoc repository[/bold underline]")
        raise typer.Exit(code=1)

    # Create the repository
    print(f"Initializing andoc repository at \"{os.path.abspath(path)}\"")
    os.mkdir(os.path.join(path, 'andoc'))

    # Add the .andoc to the .gitignore file
    if add_to_gitignore:
        if os.path.isfile(os.path.join(path, '.gitignore')):
            with open(os.path.join(path, '.gitignore'), 'a') as f:
                f.write(f"\nandoc")
        else:
            with open(os.path.join(path, '.gitignore'), 'w') as f:
                f.write(f"andoc")


def path_callback(ctx: typer.Context, path: str) -> Path | None:
    if ctx.resilient_parsing:
        return
    
    route = Path(path).resolve()

    if not route.exists():
        printerr(f"[red]Invalid path:[/red] {path} does [bold underline]not exist[/bold underline]") 
        raise typer.BadParameter(path)

    return route

@app.command()
def add_doc(
    path: Annotated[
        Path,
        typer.Argument(
            help="(str) 📂 The path to the object to add documentation to.",
            rich_help_panel="Optional Arguments",
            callback=path_callback
        ) # type: ignore
    ],

    line: Annotated[
        Optional[int],
        typer.Argument(
            help="(int) 🏷️ The line number to add the documentation to.",
            rich_help_panel="Optional Arguments"
        ) # type: ignore
    ] = None,

    # doc
    # tags
    # message

    add_to_gitignore: Annotated[
        bool,
        typer.Option(
            help="(bool) 🤫 Whether to add the andoc directory to the .gitignore file.",
        ) # type: ignore
    ] = False,
):
    """
    Adds documentation to the specified file.
    """
    route = Path(path).resolve()

    if not route.exists():
        printerr(f"[red]Invalid path:[/red] {path} does [bold underline]not exist[/bold underline]") 
        raise typer.Exit(code=1)

    try:
        andoc_folder = path_to_andoc_folder(route)
    except Exception:
        printerr(f"[red]Invalid path:[/red] {path} is [bold underline]not an andoc repository[/bold underline]")
        raise typer.Exit(code=1)

    doc_file = (andoc_folder / route.name).with_suffix('.andoc')
    print(route)
    print(andoc_folder)
    if doc_file.exists():
        return
    else:
        doc_file.touch()


if __name__ == '__main__':
    app()