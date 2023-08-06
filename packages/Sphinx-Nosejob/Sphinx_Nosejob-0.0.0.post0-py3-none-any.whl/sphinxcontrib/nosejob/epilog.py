"""
Often one needs to provide a common set of substitutions for their restructured text.
Sphinx allows one to make these available during document compilation by setting the ``epilog`` attribute within their configuration file.
While this works fine for the odd standalone project it becomes a little cumbersome if one has to support multiple projects with a common set of substitutions.

This module provides the means for storing ones epilog in an external file instead which may then be shared across ones projects.
It also provides a default epilog with more generic terms and substitutions.

.. To be merged with the previous paragraph or deleted...
.. This package allows one to separate these substitutions out from the Sphinx configuration file and into a separate, dedicated, file.
.. One may then share this between their projects, typically via symbolic link(s), to provide a common set of substitutions to their RsT documents.

One uses the following functions to set the ``epilog`` attribute within the Sphinx configuration file.
Each function loads and concatentates the filenam(s) it is given with the epilog provided by the package and this is then set as the epilog for ones project.

The package provided epilog contains the following contents.

.. literalinclude:: ../../nosejob/epilog.rst
  :language: rest
  
"""
from pathlib import Path
from itertools import chain
import pkg_resources

def epilog(text, *paths, shared = True):
 """Combines the provided text, projects epilog and the one provided by Nose Job into a singe epilog during sphinx compilation
 
 This loads the specified file(s), optionally appending the package epilog for use within ones Sphinx documentation.
 
 Arguments:
  text    The project specific epilog
  paths   The path(s) to ones local epilog(s)
  shared  A flag that appends the package supplied epilog. 
 """
 for path in paths :
  with open(path) as file :
   text = "\n".join([text, file.read()])
 if shared :
  # Using Package Data : https://stackoverflow.com/a/779552/958580
  with open(pkg_resources.resource_filename(__package__, "epilog.rst")) as file :
   text = "\n".join([text, file.read()])
  # Originally : 
#   with Path(__file__).with_suffix(".rst").open() as file :
#    data += file.read()
  # Initially I had placed the file, epilog.rst, under a folder
  # called epilog. This code would then load it and supposedly
  # any further files that were present in the folder. This was
  # never tested but the code is kept in case it becomes useful.
#  for path in chain(Path(__file__).with_suffix("").iterdir()) :
#   with path.open() as file : 
#    data += file.read()
 return text

def epilogs(*paths, shared = True):
 """DEPRECATED : This loads the specified file(s), optionally appending the package epilog for use within ones Sphinx documentation.
 
 Arguments:
  paths   The path(s) to ones local epilog(s)
  shared  A flag that appends the package supplied epilog. 
 """
 data = ""
 for path in paths :
  with open(path) as file : 
   data += file.read()
 if shared :
  with Path(__file__).with_suffix(".rst").open() as file :
   data += file.read()
 return data

