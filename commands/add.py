import typer
import commands.add_commands.doc as doc
import commands.add_commands.bookmark as bookmark

app = typer.Typer()

app.add_typer(doc.app, name="doc")
app.add_typer(bookmark.app, name="bookmark")
