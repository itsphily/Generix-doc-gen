import typer

from .check import app as check_app
from .generate import app as generate_app
from .list import app as list_app
from .update import app as update_app

app = typer.Typer(help="AI-powered documentation generator.", no_args_is_help=True)

# Single commands - flattens to top level
app.add_typer(generate_app)
app.add_typer(list_app)
app.add_typer(check_app)
app.add_typer(update_app)
