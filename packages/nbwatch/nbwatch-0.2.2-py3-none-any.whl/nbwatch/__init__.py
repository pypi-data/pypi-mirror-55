"""Preview IPython notebooks in your browser.

Usage:
  nbwatch -h | --help
  nbwatch -V | --version
  nbwatch [-x | --execute] [-v | --verbose] <file>

Options:
  -h --help     Show this screen.
  -x --execute  Execute code cells in this notebook.
  -V --version  Display the version number.
  -v --verbose  Increase verbosity (lower logging level).
"""

__version__ = '0.2.2'

import logging
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from docopt import docopt

from flask import (
    Flask, Response, render_template, request
)

from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

import nbformat


app = Flask(__name__)

exporter = HTMLExporter()
exporter.template_file = 'basic'

preprocessor = ExecutePreprocessor(timeout=600)


arguments = docopt(
    __doc__,
    version=f'nbwatch {__version__}'
)

exports = defaultdict(str)
execute = arguments.get('--execute')
source = Path(arguments.get('<file>'))

logger = logging.getLogger('werkzeug')

if arguments.get('--verbose'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.CRITICAL)


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
    while path.exists():
        last_modified = exports['last_modified'] or 0
        time.sleep(.5)
        if path.stat().st_mtime > last_modified:
            print('Change detected!')
            contents = read_final(path)
            notebook = nbformat.reads(contents, as_version=4)
            if execute:
                preprocessor.preprocess(
                    notebook, {'metadata': {'path': str(path.parent)}}
                )
            body, resources = exporter.from_notebook_node(notebook)
            exports['body'] = body
            exports['inlining'] = '\n'.join(
                resources['inlining']['css']
            )
            print('Reloading...')
            yield f'data: \n\n'
            exports['last_modified'] = path.stat().st_mtime


@app.route('/')
def index():
    """Single route for notebook template and event stream."""
    if request.headers.get('accept') == 'text/event-stream':
        return Response(watch(source), content_type='text/event-stream')
    else:
        return render_template(
            'index.html',
            body=exports['body'],
            inlining=exports['inlining']
        )


def run():
    """Entry point for shell command."""
    app.run(debug=False)
