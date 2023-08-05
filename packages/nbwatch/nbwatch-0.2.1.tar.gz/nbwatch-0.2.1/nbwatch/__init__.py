"""Preview IPython notebooks in your browser.

Usage:
  nbwatch <file>

Options:
  -h --help  Show this screen.
  --version  Display the version number.
"""

__version__ = '0.2.1'

import time
import base64

import nbformat

from pathlib import Path
from typing import Iterator
from collections import defaultdict

from docopt import docopt
from nbconvert import HTMLExporter
from flask import (
    Flask, Response, request, render_template
)


app = Flask(__name__)

exporter = HTMLExporter()
exporter.template_file = 'basic'

arguments = docopt(
    __doc__,
    version=f'nbwatch {__version__}'
)
exports = defaultdict(str)
source = Path(arguments.get('<file>'))


def read_final(path: Path) -> str:
    """
    Repeatedly read the file until it is non-empty.
    Some notebook editors empty the source file before updating it.
    """
    contents = ''
    while len(contents) == 0:
        with path.open() as file:
            contents = file.read()
    return contents


def watch(path: Path) -> Iterator[str]:
    """
    Watch the provided notebook for changes.
    Update the body each time a change is detected, then trigger a page reload.
    """
    last_modified = 0
    while path.exists():
        time.sleep(.5)
        if path.stat().st_mtime > last_modified:
            contents = read_final(path)
            notebook = nbformat.reads(contents, as_version=4)
            body, resources = exporter.from_notebook_node(notebook)
            exports['body'] = body
            exports['inlining'] = '\n'.join(
                resources['inlining']['css']
            )
            yield f'data: \n\n'
            last_modified = path.stat().st_mtime


@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        return Response(watch(source), content_type='text/event-stream')
    return render_template(
        'index.html',
        body=exports['body'],
        inlining=exports['inlining']
    )


def run():
    app.run(debug=False)
