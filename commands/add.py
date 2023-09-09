from pathlib import Path
from typing import Annotated, Optional
from uuid import UUID
import uuid
import typer
from models.methods.andoc_repository import path_to_andoc_repository

app = typer.Typer(
    rich_markup_mode="rich",
    help="➕ Program to add documentation to files and directories.",
    no_args_is_help=True,
)

"""
andoc add doc --> mostrar el help del comando
andoc add doc <file || directory> --> añadir la documentación que hace referencia al archivo o directorio como tal
andoc add doc -p <file || directory> --> añadir la documentación que hace referencia al archivo o directorio como tal
andoc add doc (-p <file || directory>)... --> añadir la documentación que hace referencia a todos los archivos o directorios especificados
andoc add doc <file> --bookmark --> añadir la documentación a todos los bookmarks del archivo
andoc add doc -p <file> --bookmark --> añadir la documentación a todos los bookmarks del archivo
andoc add doc (-p <file>)... --bookmark --> añadir la documentación a todos los bookmarks de todos los archivos especificados
andoc add doc <bookmark> --> añadir la documentación al bookmark con el uuid especificado
andoc add doc -b <bookmark> --> añadir la documentación al bookmark con el uuid especificado
andoc add doc <bookmark>... --> añadir la documentación a todos los bookmarks con los uuids especificados
andoc add doc (-b <bookmark>)... --> añadir la documentación a todos los bookmarks con los uuids especificados
andoc add doc -b --> añadir la documentación a todos los bookmarks sin documentación de todos los archivos
"""
@app.command(
    help="📜 Adds documentation to the specified file or directory.",
    epilog="With ❤️ by @gfranciscoerazom",
    no_args_is_help=True,
)
def doc(
    bookmark: Annotated[
        Optional[UUID],
        typer.Argument(
            help="🔢 The UUID of the documentation.",
        )
    ] = None,

    path: Annotated[
        Optional[Path],
        typer.Argument(
            help="📂 The path to the object to add documentation to.",
            exists=True,
            file_okay=True,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=True
        )
    ] = None, # Si el path es una carpeta, no se deberá pedir el uuid. Si es un archivo y se pasa el uuid solo se pedirá la documentación para ese uuid. Si es un archivo y no se pedirá la documentación para todos los uuids que tenga el archivo.

    doc: Annotated[
        Optional[str],
        typer.Argument(
            help="📝 The documentation to add.",
        )
    ] = None,

    bookmarks_list: Annotated[
        Optional[list[UUID]],
        typer.Option(
            "--bookmark",
            "-b",
            help="🔢 The UUID of the documentation.",
        )
    ] = None,

    paths_list: Annotated[
        Optional[list[Path]],
        typer.Option(
            "--path",
            "-p",
            help="📂 The path to the object to add documentation to.",
            exists=True,
            file_okay=True,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=True,
        )
    ] = None,

    docs_list: Annotated[
        Optional[list[str]],
        typer.Option(
            "--doc",
            "-d",
            help="📝 The documentation to add.",
        )
    ] = None,
):
    """
    Creates a documentation for the specified file or directory in the andoc folder.
    If the documentation file does not exist, it is created automatically with the same name as the file or directory with the extension .andoc. This files are going to have the same path as the file or directory they are documenting but inside the andoc folder.
    If the documentation file already exists, the documentation is added in ascending order by line number.
    """
    if paths_list is not None:
        doc_file_path = add_doc_file_to_andoc_repository(paths_list[0])
        doc_text = typer.prompt("Documentation")
        doc_file_path.write_text(doc_text)
        return

    # if bookmark is not None:
    #     p = Path(".").resolve()
    #     andoc_repository = path_to_andoc_repository(p)
    #     # Obtén todos los archivos del directorio actual y de sus subdirectorios
    #     for path in p.glob("**/*"):
    #         print(path)
    #     return

    # if bookmarks_list is not None:
    #     andoc_repository = path_to_andoc_repository(Path("."))
    #     return

    if bookmark is None \
      and bookmarks_list is None \
      and path       is None \
      and paths_list is None \
      and doc        is not None \
      or  docs_list  is not None:
        raise typer.BadParameter("You must specify the path to the file or directory or a uuid to add the documentation to.")

    # if paths_list is not None:
    #     for path in paths_list:
    #         add_doc_file_to_andoc_repository(path)

def add_doc_file_to_andoc_repository(path: Path):
    andoc_repository = path_to_andoc_repository(path)

    # Divide the path into its components
    andoc_repository_parts = andoc_repository.parts
    path_parts = path.parts

    # Remove the common parts
    i = 0
    for i in range(len(andoc_repository_parts)):
        if andoc_repository_parts[i] != path_parts[i]:
            break

    path_parts = andoc_repository_parts + path_parts[i:]

    path = Path(*path_parts)

    path.parent.mkdir(parents=True, exist_ok=True)
    path = path.with_suffix(f"{path.suffix}.andoc")
    path.touch(exist_ok=True)
    return path


@app.command(
    help="🔖 Adds a bookmark to the specified line in a file.",
    epilog="With ❤️ by @gfranciscoerazom",
    no_args_is_help=True,
)
def bookmark(
    file: Annotated[
        typer.FileText,
        typer.Argument(
            help="📄 The file to add the bookmark to.",
            mode="r+",
            encoding="utf-8",
        )
    ],

    line: Annotated[
        int,
        typer.Argument(
            help="🔢 The line to add the bookmark to.",
            min=1,
        )
    ],

    prefix: Annotated[
        str,
        typer.Option(
            "--prefix",
            "-p",
            help="🔖 The prefix to add to the bookmark.",
        )
    ] = "",

    postfix: Annotated[
        str,
        typer.Option(
            "--postfix",
            "-s",
            help="🔖 The postfix to add to the bookmark.",
        )
    ] = ""
):
    """
    Adds a bookmark to the specified line in a file.
    """
    doc_uuid = uuid.uuid4()

    data = file.readlines()
    data.insert(line, f"{prefix}andoc: {doc_uuid}{postfix}\n")
    file.seek(0)
    file.writelines(data)
    file.close()
