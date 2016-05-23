'''Py-LeRi (pyleri) Python LR-parsing module.

This module is inspired by lrparsing (http://lrparsing.sourceforge.net/),
a Python parser written by Russell Stuart, 2014-05-29.

We did however found some strange, conflict behavior using this module and
therefore decided to build our own parser which works together with the
Javascript JS-LeRi (jsleri) module so we can exchange grammars written by this
module with JavaScript projects.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
:license: need to decide


Changelog

Version 1.1.2
    - Fixed export_c() to support Ref(). An update to cleri is not needed since
      in C we can simply pre-define a variable and later assign the actual
      object.
Version 1.1.0
    - Added Ref() support which can be used to create forward references.
    - Updated jsleri to support Ref() and updated export_js() method to support
      this new class.
'''

from .choice import Choice
from .grammar import Grammar
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
    NameAssignedError)

__author__ = 'Jeroen van der Heijden'
__maintainer__ = 'Jeroen van der Heijden'
__email__ = 'jeroen@transceptor.technology'
__version__ = '1.1.2'
