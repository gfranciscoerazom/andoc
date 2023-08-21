from typing_extensions import Annotated
from rich import print
from rich.console import Console
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
        )
    ] = '.',
    add_to_gitignore: Annotated[
        bool,
        typer.Option(
            help="(bool) Whether to add the andoc directory to the .gitignore file.",
        )
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


@app.command()
def rm_andoc(path: str = '.'):
    pass


if __name__ == '__main__':
    app()