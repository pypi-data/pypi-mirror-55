from docutils import nodes

class pathTree(nodes.Admonition, nodes.Element) : # (nodes.Structural, nodes.Element) :
 """
 Combines Admonition and Element into a single class
 """
# class dirtrees(nodes.General, nodes.Element) :

# class path(nodes.Structural, nodes.Element) : # (nodes.Admonition, nodes.Element)
#  """
#  Combines Admonition and Element into a single class
#  """
# # class dirtrees(nodes.General, nodes.Element) :
# 
# class text(nodes.Structural, nodes.Element) : # (nodes.Admonition, nodes.Element)
#  """
#  Combines Admonition and Element into a single class
#  """
# # class dirtrees(nodes.General, nodes.Element) :

def visit_pathtree_node(self, node) :
 self.visit_admonition(node)

def depart_pathtree_node(self, node) :
 self.depart_admonition(node)
