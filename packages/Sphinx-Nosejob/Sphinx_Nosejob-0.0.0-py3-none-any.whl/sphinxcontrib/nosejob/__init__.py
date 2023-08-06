"""
sphinxcontrib.nosejob
---------------------

A collection of directives to compliment those provided by sphinx
"""
# Meta Information
from sphinxcontrib.__meta__ import *
# from . import trees
from .epilog import epilog, epilogs # This is perhaps a little dicy as it relies on Python searching for epilog within the init file before the package
# Features
from . import database
from . import trees

# if False:
#     # For type annotations
#     from typing import Any, Dict  # noqa
#     from sphinx.application import Sphinx  # noqa

# import pbr.version
# __version__ = pbr.version.VersionInfo('nosejob').version_string() # TODO : Use pkg_resources, place into a __meta__.py file.

def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    # app.add_directive("tree", trees.Tree)

    # Features
    database.setup(app)
    trees.setup(app)

    # Registration
    return {'parallel_read_safe' : True,
            'parallel_write_safe': True,
            'version'            : __version__}
