from docutils.parsers.rst import Directive
from docutils import nodes
from sphinxcontrib.nosejob.trees.nodes import pathTree
from sphinx.locale import _

class PathTree(Directive) :
 """ A directive generating Path Trees with annotations/commnetary
 
 This is useful for describing the structure of a package or a folder.
 At a pinch this may also be co-erced into describing the routing for a website (Support for this is intended in the future).
 """

 #: This directive has no required arguments
 required_arguments        = 0    # This is moot but ensures the default is enforced
 #: A relative path may be given as the optional argument. 
 #: This path specifies root path for the folders depicted by the directive.
 #: Future implementaitons might use this path to ensure that the listed paths are valid.
 optional_arguments        = 1    # Allow for a root path to be specified
 #: Allowing the final/only optional argument to include white space the user does not need to escape *root* paths that contain spaces
 final_argument_whitespace = True # Allow the optional argument to be a path containing spaces, without the need for quotes
 #: The directive accepts a block of code containing a list of paths and one liners explaining their purpose.
 has_content               = True # Allows the directive to have "body" text
 #: Only the stock options for a directive are supported.
 #: No additional options are catered for under the current implementation.
 option_spec               = {}   # Incase I need to support arguments later on.

 def run(self) :
  """ The execution function for the directive """
  # Environmental Instance
  environment = self.state.document.settings.env
  # Target Element
  target_name = "pathtree-%d" % environment.new_serialno('pathtree') # Number the occurence
  target_node = nodes.target('','',ids=[target_name])
  # Pathtree Node
  tree_node =  pathTree(self.content)
  tree_node += nodes.title(_("Path Tree"),_("Path Tree"))
  # Process/Parse the directive
  self.state.nested_parse(self.content, self.content_offset, tree_node)
   
  return [target_node, tree_node]

class Tree(Directive) :
    """Provides a directive for tabulating trees"""
    # Note : This is to be meregd with the PathTree Directive in due course

    def run(self):
        node = nodes.paragraph(text="Tree")
        return [node]

__all__ = ["Tree", "PathTree"]
