#!/usr/bin/env python
"""Meta Data

Specifies the legal, editorial and contact information for the project.

:pep:`0440` prescribes the structure of versioning information in a standard Python package.
"""
from datetime import datetime

# Corporate Information
__company__     = "Manaikin"
__website__     = "manaikin.com"

# Project Information
__project__     = "Sphinx-NoseJob:Trees"
__description__ = "Sphinx directives for representing trees"

# Legal Information
__copyright__   = f"Copyright 2019 - {datetime.now().year} of {__company__}"
__licence__     = "To be decided"

# Editorial Information
__author__      = "Carel van Dam"
__authors__     = [] # List of additional contributors
__editor__      = "{author}".format(author = __author__)
__email__       = "carelvdam@gmail.com"  # Maintainer>Editor>Author e-mail address
__credits__     = [__author__, *__authors__]
__maintainer__  = __editor__

# Version Information
__release__ = (0,0,0)           #: The release number, major.minor.micro, serves as the package version number in :file:`setup.py`
__version__ = __release__[:-1]  #: The version number, major.minor, used predominantly within documentation
__dialect__ = None              #: The version dialect or epoch indicates the numbering scheme.
__entrant__ = (None, None)      #: The release candidate, product status or entrant, aX|bX|rcX for alpha|beta|release candidate respectively.
__develop__ = None              #: The development revision, .devX, for minor bug fixes but no API changes.
__postnum__ = None              #: The post revision, .postX, for quick pushes where files and the like were accidentally excluded

__version__ = ".".join([str(item) for item in __version__]) # The effective version number for comparative purposes
__release__ = "{}!".format(__dialect__) if __dialect__ is not None else "" \
            + ".".join([str(item) for item in __release__]) \
            + {None    : lambda value : "".format(value)     if value is not None else "",
               "Alpha" : lambda value : "a{}".format(value)  if value is not None else "",
               "Beta"  : lambda value : "b{}".format(value)  if value is not None else "",
               "RC"    : lambda value : "rc{}".format(value) if value is not None else "",}[__entrant__[0]](__entrant__[1]) \
            + (".post{}".format(__postnum__) if __postnum__ is not None else "") \
            + (".dev{}".format(__develop__)  if __develop__ is not None else "") # The effective release number conforming to the mask [N!]N(.N)*[{a|b|rc}N][.postN][.devN]

__all__ = [
    # Corporate Information
    "__company__",
    "__website__",
    # Project Information
    "__project__",
    "__description__",
    # Version Information
    "__release__",
    "__version__",
    # Legal Information
    "__copyright__",
    "__licence__",
    # Editorial Information
    "__author__",
    "__authors__",
    "__editor__",
    "__email__",
    "__credits__",
    "__maintainer__"]
