import argparse
from pathlib import Path
import sys
from .server import app, settings


def run():
    argparser = argparse.ArgumentParser(
        description="Tool to serve a set of Wok files using a Notion-like template.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argparser.add_argument(
        "-d",
        "--dir",
        type=str,
        help="directory containing the wok files",
        required=True,
    )
    argparser.add_argument(
        "-b",
        "--host",
        type=str,
        help="host to bind to for http requests",
        default="localhost",
    )
    argparser.add_argument(
        "-p",
        "--port",
        type=int,
        help="port to bind to for http requests",
        default=8080,
    )

    args = argparser.parse_args()

    files_path = Path(args.dir)
    if not files_path.is_dir():
        print(f"ERR: Path {args.dir} isn't a directory")
        sys.exit(1)

    settings["files_path"] = files_path.absolute()
    app.run(host=args.host, port=args.port, debug=True)
