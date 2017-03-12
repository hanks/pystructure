|Build Status| |Coverage Status|

pystructure
===========

A tiny tool to help reading source code with showing structure of python
source code

Why
===

I use PyCharm as my python IDE, and sometimes I can use ``structure``
navigation view to check code structure easily, like below:

.. figure:: https://github.com/hanks/pystructure/blob/master/docs/images/pycharm-structure.jpg?raw=true
   :alt: structure

   structure

It is useful when you read some open source codes, and for me, I like to
write memo for code structure down in my note, but you can not copy the
structure information to text from PyCharm, so I create this tool to
help me easily to output text version of structure of python code.

Installation
============

``pip install pystructure``

Usage
=====

::

    > pystructure

    Usage:
        pystructure.py SRC_PATH [-o FILE | --output=FILE]

::

    > pystructure pystructure.py

    v __VERSION__
    c PYSymbol(object)
      v GLOBAL_VAR
      v FUNCTION
      v CLASS
      v METHOD
      v ATTRIBUTE
      v PRIVATE_METHOD
    c PYStructureVisitor(object)
      v PREFIX
      v LITERAL_VALUE_PREFIX
      f __init__(self)
      f visit(self, node_list)
      f visit_Assign(self, node)
      f visit_ClassDef(self, node)
      f visit_FunctionDef(self, node)
      f visit_literal_Num(self, node)
      f visit_literal_Name(self, node)
      f visit_literal_Str(self, node)
      f visit_literal_List(self, node)
      f visit_literal_Tuple(self, node)
      f visit_literal_Dict(self, node)
      f _get_visit_result(self, node, prefix="PREFIX")
      f _get_literal_value_list(self, node_list)
      f _build_func_signature(self, func_name, args_list, default_list, kwarg, vararg)
      f method_dict(self)
    c StructureParser(object)
      f __init__(self)
      f accept(self, visitor)
      f load(self, src)
      f export(self)
      f _format_structure(self, root, level=0, output=None)
    f main()

Implementation
==============

-  ast - Build-in python library, to do static analytic for the source
   code
-  docopt - A great tool to help to create beautiful CLI for you

Contribution
============

1. Fork the repository on GitHub.
2. Make a branch off of master and commit your changes to it.
3. Run the tests with tox

-  Either use tox to build against all supported Python versions (if you
   have them installed) or use tox -e py{version} to test against a
   specific version, e.g., tox -e py27 or tox -e py33.

4. Submit a Pull Request to the master branch on GitHub.

If you’d like to have a development environment for ``pystructure``, you
should create a virtualenv and then do ``pip install -e .`` from within
the directory.

Lisence
=======

MIT Lisence

.. |Build Status| image:: https://travis-ci.org/hanks/pystructure.svg?branch=master
   :target: https://travis-ci.org/hanks/pystructure
.. |Coverage Status| image:: https://coveralls.io/repos/github/hanks/pystructure/badge.svg?branch=master
   :target: https://coveralls.io/github/hanks/pystructure?branch=master
