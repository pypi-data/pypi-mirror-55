"""

Indices
-------

One may include the table, `tableindex`, and field, `fieldindex`, indices as follows within their :file:`index.rst` file as follows ::

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`tableindex`
    * :ref:`fieldindex`
    * :ref:`modindex`
    * :ref:`search`

.. note ::

    This code is adapted from the Sphinx and Opensource.com
"""
# TODO : Clean up the cross referencing between tables and fields
# TODO : Clean up the API for fields listing the tables that they are a part of and tables listing the fields that they are a part of
import docutils
from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives

import sphinx
from sphinx.domains import Domain, Index
from sphinx.domains.std import StandardDomain
from sphinx.roles import XRefRole
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx import addnodes

from collections import namedtuple

# Original Naming            name   sig         typ    docname     anchor      prio
# Conventional Naming        name   signature   type   document    anchor      priority
Table = namedtuple("Table",("name","signature","type","document", "reference","priority"))
Field = namedtuple("Field",("name","signature","type","document", "reference","priority"))

class TableDirective(ObjectDescription):
    """A custom directive that describes a database table

    HTML
        This creates a table where the signature is wrapped into the header of the table and the content within the body.
    LaTeX
        Not sure how this affects the output.
    Text
        Not sure how this affects the output.
    """

    required_arguments = 1

    option_spec = {
        'fields': directives.unchanged_required
    }

    def handle_signature(self, sign, node):
        node += addnodes.desc_name(text=sign)
        node += addnodes.desc_type(text='(Table)')
        return sign

    def add_target_and_index(self, name, sign, node):
        # Set the ID upon the node element
        node['ids'].append('table' + '-' + sign)
        # The following creates the references from the tables to the fields and back again.
        if 'noindex' not in self.options:
            name = "{}.{}.{}".format('db', type(self).__name__, sign)
            imap = self.env.domaindata['db']['tables2fields']
            imap[name] = imap.get(name,set()) | set(self.options.get('fields','').split(' '))
            objs = self.env.domaindata['db']['tables']
            objs.append(Table(name,
                              sign,
                              'Table',
                              self.env.docname,
                              'table' + '-' + sign,
                              0))


class FieldDirective(ObjectDescription):
    """A custom directive that describes a database field


    .. rst:directive:: .. db:field:: FIELD

        Provides a description for a database field.
        This may be references through the :rst:role:`db:field` role.

    .. rst:role:: :db:field:`FIELD`

        Provides a reference to the field described by :rst:dir:`db:field`

    HTML
        This creates a table where the signature is wrapped into the header of the table and the content within the body.
    LaTeX
        Not sure how this affects the output.
    Text
        Not sure how this affects the output.
    """

    required_arguments = 1

    option_spec = {
        'spec': directives.unchanged_required
    }

    def handle_signature(self, sign, node):
        try : # ObjectDescription simply raises a ValueError
            super().handle_signature(sign, node)
        except ValueError :
            pass
        node += addnodes.desc_name(text=sign)
        node += addnodes.desc_type(text='(Field)')
        if self.options.get('spec',None) :
            node += addnodes.desc_annotation(self.options.get('spec'))
        return sign

    def add_target_and_index(self, name, sign, node):
        node['ids'].append('field' + '-' + sign)
        from pprint import pprint
        # print(self.state)
        # pprint(dir(self.state))
        # print(self.state.parent)
        # print(self.state.parent.parent)
        # pprint(node.parent.attlist)
        # pprint(sign)
        # pprint(node.parent.parent.attributes)
        # pprint(node.parent.attributes)
        # pprint(node.attributes)
        # pprint([item for item in node.traverse(condition = lambda node : node.attributes["objtype"] == "table")])
        # pprint(dir(node.parent))
        # print(help(node._all_traverse))
        # print(help(node._fast_traverse))
        # print(help(node.parent))
        # print(help(node.traverse))
        # print(help(node.walk))
        # print(help(node.walkabout))
        # The following creates the references from the tables to the fields and back again.
        if 'noindex' not in self.options:
            # New Code
            name = "{}.{}.{}".format('db', type(self).__name__, sign)
            imap = self.env.domaindata['db']['fields2tables']
            imap[name] = imap.get(name,set()) | set(self.options.get('tables','').split(' '))
            objs = self.env.domaindata['db']['fields']
            objs.append(Field(name,
                              sign,
                              'Field',
                              self.env.docname,
                              'field' + '-' + sign,
                              0))


class FieldIndex(Index):
    """A custom directive that creates an ingredient matrix."""

    name = 'fields'
    localname = 'Field Index'
    shortname = 'Fields'

    def __init__(self, *args, **kwargs):
        super(FieldIndex, self).__init__(*args, **kwargs)

    def generate(self, docnames=None):
        """Return entries for the index given by *name*.  If *docnames* is
        given, restrict to entries referring to these docnames.
        The return value is a tuple of ``(content, collapse)``, where
        * collapse* is a boolean that determines if sub-entries should
        start collapsed (for output formats that support collapsing
        sub-entries).
        *content* is a sequence of ``(letter, entries)`` tuples, where *letter*
        is the "heading" for the given *entries*, usually the starting letter.
        *entries* is a sequence of single entries, where a single entry is a
        sequence ``[name, subtype, docname, anchor, extra, qualifier, descr]``.
        The items in this sequence have the following meaning:
        - `name` -- the name of the index entry to be displayed
        - `subtype` -- sub-entry related type:
          0 -- normal entry
          1 -- entry with sub-entries
          2 -- sub-entry
        - `docname` -- docname where the entry is located
        - `anchor` -- anchor for the entry within `docname`
        - `extra` -- extra info for the entry
        - `qualifier` -- qualifier for the description
        - `descr` -- description for the entry
        Qualifier and description are not rendered e.g. in LaTeX output.
        """

        content = {}

        objs = {name: (dispname, typ, docname, anchor)
                for name, dispname, typ, docname, anchor, prio
                in self.domain.get_objects()}

        imap = {}
        fields = self.domain.data['tables2fields']
        for name, ingr in fields.items():
            for ig in ingr:
                imap.setdefault(ig, [])
                imap[ig].append(name)

        for ingredient in imap.keys():
            lis = content.setdefault(ingredient, [])
            objlis = imap[ingredient]
            for objname in objlis:
                dispname, typ, docname, anchor = objs[objname]
                lis.append((
                    dispname, 0, docname,
                    anchor,
                    docname, '', typ
                ))
        re = [(k, v) for k, v in sorted(content.items())]

        return (re, True)


class TableIndex(Index):
    name = 'tables'
    localname = 'Table Index'
    shortname = 'Tables'

    def __init__(self, *args, **kwargs):
        super(TableIndex, self).__init__(*args, **kwargs)

    def generate(self, docnames=None):
        """Return entries for the index given by *name*.  If *docnames* is
        given, restrict to entries referring to these docnames.
        The return value is a tuple of ``(content, collapse)``, where
        * collapse* is a boolean that determines if sub-entries should
        start collapsed (for output formats that support collapsing
        sub-entries).
        *content* is a sequence of ``(letter, entries)`` tuples, where *letter*
        is the "heading" for the given *entries*, usually the starting letter.
        *entries* is a sequence of single entries, where a single entry is a
        sequence ``[name, subtype, docname, anchor, extra, qualifier, descr]``.
        The items in this sequence have the following meaning:
        - `name` -- the name of the index entry to be displayed
        - `subtype` -- sub-entry related type:
          0 -- normal entry
          1 -- entry with sub-entries
          2 -- sub-entry
        - `docname` -- docname where the entry is located
        - `anchor` -- anchor for the entry within `docname`
        - `extra` -- extra info for the entry
        - `qualifier` -- qualifier for the description
        - `descr` -- description for the entry
        Qualifier and description are not rendered e.g. in LaTeX output.
        """

        content = {}
        items = ((name, dispname, typ, docname, anchor)
                 for name, dispname, typ, docname, anchor, prio
                 in self.domain.get_objects())
        items = sorted(items, key=lambda item: item[0])
        for name, dispname, typ, docname, anchor in items:
            lis = content.setdefault('Table', [])
            lis.append((
                dispname, 0, docname,
                anchor,
                docname, '', typ
            ))
        re = [(k, v) for k, v in sorted(content.items())]

        return (re, True)


class DatabaseDomain(Domain):
    name = 'db'
    label = 'Database'

    roles = {
        # The following map to XRefRole which simply maps back to self.resolve_xref
        'table': XRefRole(),
        'field': XRefRole(),
    }

    directives = {
        'table': TableDirective,
        'field': FieldDirective,
    }

    indices = {
        TableIndex,
        FieldIndex
    }

    initial_data = {
        # Stores the mapping
        'fields2tables': {},
        'tables2fields': {},  # name -> object  : The original storage for fields
        # Stores the references
        'tables': [],         # object list     : The original field for tables
        'fields': [],
    }

    def get_full_qualified_name(self, node):
        """Return full qualified name for a given node"""
        return "{}.{}.{}".format('db',
                                 type(node).__name__,
                                 node.arguments[0])

    def get_objects(self):
        # A convenience function for getting a list of table and field references
        for obj in self.data['tables'] + self.data['fields']:
            yield (obj)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):

        match = [(docname, anchor)
                 for name, sig, typ, docname, anchor, prio
                 in self.get_objects() if sig == target]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]

            return make_refnode(builder, fromdocname, todocname,
                                targ, contnode, targ)
        else:
            print("Awww, found nothing")
            return None



def setup(app):
    app.add_domain(DatabaseDomain)

    StandardDomain.initial_data['labels']['tableindex'] = ('db-tables', '', 'Table Index')
    StandardDomain.initial_data['labels']['fieldindex'] = ('db-fields', '', 'Field Index')

    StandardDomain.initial_data['anonlabels']['tableindex'] = ('db-tables', '')
    StandardDomain.initial_data['anonlabels']['fieldindex'] = ('db-fields', '')

    return {'version': '0.1'}
