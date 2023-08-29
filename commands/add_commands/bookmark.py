from typing_extensions import Annotated
import uuid
import typer


app = typer.Typer()


@app.callback(
    help="🔖 Adds a bookmark to the specified line in a file.",
    epilog="With ❤️ by @gfranciscoerazom",
    invoke_without_command=True,
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
