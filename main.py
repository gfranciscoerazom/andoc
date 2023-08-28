from typing_extensions import Annotated
import commands.add_doc as add_doc
import commands.init as init
import typer

from constants.strings.rich_format import BOLD_UNDERLINE


__VERSION__ = "0.1.0"


app = typer.Typer(
    help="📚 A documentation tool to manage the documentation of a project independently of the project itself.",
    rich_markup_mode="rich",
    epilog=f"With ❤️ by {BOLD_UNDERLINE%'@gfranciscoerazom'}",
)

app.add_typer(init.app, name="init")
app.add_typer(add_doc.app, name="add-doc")


@app.callback(
    invoke_without_command=True
)
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="📜 Shows the current version of andoc.",
            rich_help_panel="Optional Arguments",
            is_eager=True
        )
    ] = False
):
    """
    A documentation tool to manage the documentation of a project independently of the project itself.
    """
    if version:
        typer.echo(f"andoc version {__VERSION__}")


if __name__ == '__main__':
    app()