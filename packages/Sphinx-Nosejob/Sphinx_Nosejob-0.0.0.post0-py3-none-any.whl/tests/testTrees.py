"""
Testing Forrestry
=================

[1] covers the difference between the stock testing methods used by sphinx and those provided by the sphinx-testing module.
[2], [3] and [4] further illustrate the differences while [5] illustrates how to test roles.

[1] https://github.com/sphinx-doc/sphinx/issues/2277
[2] https://chromium.googlesource.com/infra/third_party/Sphinx/+/refs/heads/master/tests/test_directive_code.py
[3] https://github.com/blockdiag/sphinxcontrib-blockdiag/blob/master/tests/test_html.py
[4] https://github.com/sphinx-doc/sphinx/blob/master/tests/test_ext_todo.py
[5] https://github.com/sphinx-doc/sphinx/blob/master/tests/test_ext_todo.py
"""
# import pytest
from unittest import TestCase, main
# from pathlib import Path
# from sphinx.util import docutils
from sphinx_testing import with_app

# path = Path("tests/docs/basic/").resolve()

class testTrees(TestCase): 

    @with_app(buildername="html",srcdir="documents", copy_src_dir_to_tmpdir=True, confoverride={"master_doc" : "trees"})
    def testTrees(self, app, status, warning):
        app.build()
        html = (app.outdir/'trees')
    
# PyTest tests
# @pytest.mark.sphinx('html', testroot = "testTrees", freshenv = True, confoverrides={"trees_include_trees":True})
# def testTree(app, status, warning):
#     # app.connect()
#     app.builder.build_all()

# @with_app(buildername="html", srcdir=path)
# @pytest.mark.sphinx("html")
# def test_build_html(app, status, warning) :
#   app.builder.build_all()

# @with_app(buildername="singlehtml", srcdir=path)
# def test_build_html(app, status, warning) :
#   app.builder.build_all()
# 
# @with_app(buildername="latex", srcdir=path)
# def test_build_html(app, status, warning) :
#   app.builder.build_all()
# 
# @with_app(buildername="epud", srcdir=path)
# def test_build_html(app, status, warning) :
#   app.builder.build_all()
# 
# @with_app(buildername="json", srcdir=path)
# def test_build_html(app, status, warning) :
#   app.builder.build_all()

if __name__ == "__main__" :
   main()