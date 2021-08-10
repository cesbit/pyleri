'''Py-LeRi (pyleri) Python LR-parsing module.

This module is inspired by lrparsing (http://lrparsing.sourceforge.net/),
a Python parser written by Russell Stuart, 2014-05-29.

We did however found some strange, conflict behavior using this module and
therefore decided to build our own parser which works together with the
Javascript JS-LeRi (jsleri) module so we can exchange grammars written by this
module with JavaScript projects.

:copyright: 2016, Jeroen van der Heijden (Transceptor Technology)
:license: MIT
'''

from .choice import Choice
from .endofstatement import end_of_statement
from .grammar import Grammar
from .grammar import create_grammar
from .keyword import Keyword
from .list import List
from .optional import Optional
from .prio import Prio
from .ref import Ref
from .regex import Regex
from .repeat import Repeat
from .sequence import Sequence
from .this import THIS
from .token import Token
from .tokens import Tokens
from .exceptions import (
    CompileError,
    KeywordError,
    ReKeywordsChangedError,
    NameAssignedError,
    MissingStartError,
    UnusedElementError,
    ParseError,
    MaxRecursionError,
)

__author__ = 'Jeroen van der Heijden'
__maintainer__ = 'Jeroen van der Heijden'
__email__ = 'jeroen@transceptor.technology'
__version__ = '1.3.4'
