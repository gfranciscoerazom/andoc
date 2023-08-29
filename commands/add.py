import typer
import commands.add.doc as doc


app = typer.Typer()

app.add_typer(doc.app, name="doc")
