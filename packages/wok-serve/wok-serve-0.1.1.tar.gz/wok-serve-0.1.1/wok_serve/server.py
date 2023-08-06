from bottle import Bottle, template, static_file, abort
from wok.parser import Parser
from wok.formatters import html_formatter
from wok.debug import print_tree
from wok.nodes import MetaNode
from pathlib import Path
import re
import pkg_resources

app = Bottle()
parser = Parser()

settings = {"files_path": ""}
static_file_path = pkg_resources.resource_filename(__name__, "static")


@app.route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_file_path)


@app.route("/")
@app.route("/<path:path>")
def render(path="/"):
    path = re.sub(r"/+", "/", path).lstrip("/")
    full_path = Path(settings["files_path"]) / path

    if full_path.is_dir() and (full_path / "index.wok").is_file():
        full_path = full_path / "index"

    full_path = str(full_path.absolute()) + ".wok"

    if not Path(full_path).is_file():
        abort(404, "File not found")

    tree = parser.parse_file(full_path, settings["files_path"])

    return render_page(tree)


def render_page(tree):
    html = html_formatter.format(tree)
    meta = tree.select("meta") or MetaNode()

    return template(
        pkg_resources.resource_string(__name__, "templates/layout.stpl").decode(
            "utf-8"
        ),
        tree=tree,
        html=html,
        meta=meta,
    )
