# Copyright (c) 2016 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A parser for Thrift IDL files.

Parser
------

Adapted from ``thriftpy.parser``.

.. autoclass:: Parser
    :members:

AST
---

.. autoclass:: Program

Headers
~~~~~~~

.. autoclass:: Include

.. autoclass:: Namespace

Definitions
~~~~~~~~~~~

.. autoclass:: Const

.. autoclass:: Typedef

.. autoclass:: Enum

.. autoclass:: EnumItem

.. autoclass:: Struct

.. autoclass:: Union

.. autoclass:: Exc

.. autoclass:: Service

.. autoclass:: ServiceReference

.. autoclass:: Function

.. autoclass:: Field

Types
~~~~~

.. autoclass:: PrimitiveType

.. autoclass:: MapType

.. autoclass:: SetType

.. autoclass:: ListType

.. autoclass:: DefinedType

Constants
~~~~~~~~~

.. autoclass:: ConstPrimitiveValue

.. autoclass:: ConstReference

Annotations
~~~~~~~~~~~

.. autoclass:: Annotation
"""
from __future__ import absolute_import, unicode_literals, print_function

from .parser import Parser
from .ast import (
    Program,
    Include,
    Namespace,
    Const,
    Typedef,
    Enum,
    EnumItem,
    Struct,
    Union,
    Exc,
    Service,
    ServiceReference,
    Function,
    Field,
    PrimitiveType,
    MapType,
    SetType,
    ListType,
    DefinedType,
    ConstValue,
    ConstPrimitiveValue,
    ConstReference,
    Annotation,
)


__all__ = [
    # Parser
    'Parser',

    # AST
    'Program',
    'Include',
    'Namespace',
    'Const',
    'Typedef',
    'Enum',
    'EnumItem',
    'Struct',
    'Union',
    'Exc',
    'Service',
    'ServiceReference',
    'Function',
    'Field',
    'PrimitiveType',
    'MapType',
    'SetType',
    'ListType',
    'DefinedType',
    'ConstValue',
    'ConstPrimitiveValue',
    'ConstReference',
    'Annotation',
]
