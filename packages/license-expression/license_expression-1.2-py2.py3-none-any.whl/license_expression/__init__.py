#
# license-expression is a free software tool from nexB Inc. and others.
# Visit https://github.com/nexB/license-expression for support and download.
#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and http://aboutcode.org
#
# This software is licensed under the Apache License version 2.0.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
This module defines a mini language to parse, validate, simplify, normalize and
compare license expressions using a boolean logic engine.

This supports SPDX license expressions and also accepts other license naming
conventions and license identifiers aliases to recognize and normalize licenses.

Using boolean logic, license expressions can be tested for equality, containment,
equivalence and can be normalized or simplified.

The main entry point is the Licensing object.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from collections import defaultdict
from collections import deque
from collections import namedtuple
from collections import OrderedDict
from copy import copy
from copy import deepcopy
from functools import total_ordering
import itertools
import re
import string

import boolean
from boolean import Expression as LicenseExpression

# note these may not all be used here but are imported here to avoid leaking
# boolean.py constants to callers
from boolean.boolean import PARSE_ERRORS
from boolean.boolean import PARSE_INVALID_EXPRESSION
from boolean.boolean import PARSE_INVALID_NESTING
from boolean.boolean import PARSE_INVALID_OPERATOR_SEQUENCE
from boolean.boolean import PARSE_INVALID_SYMBOL_SEQUENCE
from boolean.boolean import PARSE_UNBALANCED_CLOSING_PARENS
from boolean.boolean import PARSE_UNKNOWN_TOKEN

from boolean.boolean import ParseError
from boolean.boolean import TOKEN_SYMBOL
from boolean.boolean import TOKEN_AND
from boolean.boolean import TOKEN_OR
from boolean.boolean import TOKEN_LPAR
from boolean.boolean import TOKEN_RPAR

from license_expression._pyahocorasick import Trie as AdvancedTokenizer
from license_expression._pyahocorasick import Token


# Python 2 and 3 support
try:
    # Python 2
    unicode
    str = unicode  # NOQA
except NameError:
    # Python 3
    unicode = str  # NOQA


# append new error codes to PARSE_ERRORS by monkey patching
PARSE_EXPRESSION_NOT_UNICODE = 100
if PARSE_EXPRESSION_NOT_UNICODE not in PARSE_ERRORS:
    PARSE_ERRORS[PARSE_EXPRESSION_NOT_UNICODE] = 'Expression string must be unicode.'

PARSE_INVALID_EXCEPTION = 101
if PARSE_INVALID_EXCEPTION not in PARSE_ERRORS:
    PARSE_ERRORS[PARSE_INVALID_EXCEPTION] = (
        'A license exception symbol can only be used as an exception '
        'in a "WITH exception" statement.')

PARSE_INVALID_SYMBOL_AS_EXCEPTION = 102
if PARSE_INVALID_SYMBOL_AS_EXCEPTION not in PARSE_ERRORS:
    PARSE_ERRORS[PARSE_INVALID_SYMBOL_AS_EXCEPTION] = (
        'A plain license symbol cannot be used as an exception '
        'in a "WITH symbol" statement.')

PARSE_INVALID_SYMBOL = 103
if PARSE_INVALID_SYMBOL not in PARSE_ERRORS:
    PARSE_ERRORS[PARSE_INVALID_SYMBOL] = (
        'A proper license symbol is needed.')


class ExpressionError(Exception):
    pass


class ExpressionParseError(ParseError, ExpressionError):
    pass


# Used for tokenizing
Keyword = namedtuple('Keyword', 'value type')
Keyword.__len__ = lambda self: len(self.value)

# id for "with" token which is not a proper boolean symbol but an expression symbol
TOKEN_WITH = 10

# keyword types that include operators and parens

KW_LPAR = Keyword('(', TOKEN_LPAR)
KW_RPAR = Keyword(')', TOKEN_RPAR)
KW_AND = Keyword('and', TOKEN_AND)
KW_OR = Keyword('or', TOKEN_OR)
KW_WITH = Keyword('with', TOKEN_WITH)

KEYWORDS = (KW_AND, KW_OR, KW_LPAR, KW_RPAR, KW_WITH,)
KEYWORDS_STRINGS = set(kw.value for kw in KEYWORDS)

# mapping of lowercase operator strings to an operator object
OPERATORS = {'and': KW_AND, 'or': KW_OR, 'with': KW_WITH}

_simple_tokenizer = re.compile(r'''
    (?P<symop>[^\s\(\)]+)
     |
    (?P<space>\s+)
     |
    (?P<lpar>\()
     |
    (?P<rpar>\))
    ''',
    re.VERBOSE | re.MULTILINE | re.UNICODE
).finditer


class Licensing(boolean.BooleanAlgebra):
    """
    Licensing defines a mini language to parse, validate and compare license
    expressions. This is the main entry point this library.

    Some of the features are:

    - licenses can be validated against user-provided lists of known licenses
      "symbols" (such as ScanCode licenses or the SPDX list).

    - flexible expression parsing and recognition of licenses (including
      licenses with spaces and keywords (such as AND, OR WITH) or parens in
      their names).

    - in an expression licenses can be more than just identifiers such short or
      long names

    - A license can have multiple aliases (such as GPLv2 or GPL2) and each will
      be properly recognized when parsing.

    - expressions can be simplified, normalized, sorted and compared for
      containment and/or logical equivalence thanks to a built-in boolean logic
      engine.

    - Once parsed, expressions can be rendered using simple templates (for
      instance to render HTML links in a GUI).

    For example:

    >>> l = Licensing()
    >>> expr = l.parse(" GPL-2.0 or LGPL-2.1 and mit ")
    >>> expected = 'GPL-2.0 OR (LGPL-2.1 AND mit)'
    >>> assert expected == expr.render('{symbol.key}')

    >>> expected = [
    ...   LicenseSymbol('GPL-2.0'),
    ...   LicenseSymbol('LGPL-2.1'),
    ...   LicenseSymbol('mit')
    ... ]
    >>> assert expected == l.license_symbols(expr)

    >>> symbols = ['GPL-2.0+', 'Classpath', 'BSD']
    >>> l = Licensing(symbols)
    >>> expression = 'GPL-2.0+ with Classpath or (bsd)'
    >>> parsed = l.parse(expression)
    >>> expected = 'GPL-2.0+ WITH Classpath OR BSD'
    >>> assert expected == parsed.render('{symbol.key}')

    >>> expected = [
    ...   LicenseSymbol('GPL-2.0+'),
    ...   LicenseSymbol('Classpath'),
    ...   LicenseSymbol('BSD')
    ... ]
    >>> assert expected == l.license_symbols(parsed)
    >>> assert expected == l.license_symbols(expression)
    """

    def __init__(self, symbols=tuple(), quiet=True):
        """
        Initialize a Licensing with an optional `symbols` sequence of
        LicenseSymbol or LicenseSymbol-like objects or license key strings. If
        provided and this list data is invalid, raise a ValueError.
        """
        super(Licensing, self).__init__(Symbol_class=LicenseSymbol, AND_class=AND, OR_class=OR)

        # FIXME: this should be instead a super class of all symbols
        self.LicenseSymbol = self.Symbol

        symbols = symbols or tuple()

        if symbols:
            symbols = tuple(as_symbols(symbols))
            warns, errors = validate_symbols(symbols)

            if warns and not quiet:
                for w in warns:
                    print(w)

            if errors and not quiet:
                for e in errors:
                    print(e)

            if errors:
                raise ValueError('\n'.join(warns + errors))

        # mapping of known symbol key to symbol for reference
        self.known_symbols = {symbol.key: symbol for symbol in symbols}

        # mapping of known symbol lowercase key to symbol for reference
        self.known_symbols_lowercase = {symbol.key.lower(): symbol for symbol in symbols}

        # Aho-Corasick automaton-based Advanced Tokenizer
        self.advanced_tokenizer = None

    def is_equivalent(self, expression1, expression2, **kwargs):
        """
        Return True if both `expressions` LicenseExpression are equivalent.
        If a string is provided, it will be parsed and simplified.
        Extra kwargs are passed down to the parse() function.
        """
        ex1 = self._parse_and_simplify(expression1, **kwargs)
        ex2 = self._parse_and_simplify(expression2, **kwargs)
        return ex1 == ex2

    def contains(self, expression1, expression2, **kwargs):
        """
        Return True if `expression1` contains `expression2`.
        Expressions are either a string or a LicenseExpression object.
        If a string is provided, it will be parsed and simplified.

        Extra kwargs are passed down to the parse() function.
        """
        ex1 = self._parse_and_simplify(expression1, **kwargs)
        ex2 = self._parse_and_simplify(expression2, **kwargs)
        return ex2 in ex1

    def _parse_and_simplify(self, expression, **kwargs):
        expression = self.parse(expression, **kwargs)
        if expression is None:
            return None

        if not isinstance(expression, LicenseExpression):
            raise TypeError('expressions must be LicenseExpression objects: %(expression1)r, %(expression2)r' % locals())
        return expression.simplify()

    def license_symbols(self, expression, unique=True, decompose=True, **kwargs):
        """
        Return a list of LicenseSymbol objects used in an expression in
        the same order as they first appear in the expression tree.

        `expression` is either a string or a LicenseExpression object.
        If a string is provided, it will be parsed.

        If `unique` is True only return unique symbols.

        If `decompose` is True then composite LicenseWithExceptionSymbol instance are
        not returned directly but their underlying license and exception symbols are
        retruned instead.

        Extra kwargs are passed down to the parse() function.

        For example:
        >>> l = Licensing()
        >>> expected = [
        ...   LicenseSymbol('GPL-2.0'),
        ...   LicenseSymbol('LGPL-2.1+')
        ... ]
        >>> result = l.license_symbols(l.parse('GPL-2.0 or LGPL-2.1+'))
        >>> assert expected == result
        """
        expression = self.parse(expression, **kwargs)
        if expression is None:
            return []
        symbols = (s for s in expression.get_literals() if isinstance(s, BaseSymbol))
        if decompose:
            symbols = itertools.chain.from_iterable(s.decompose() for s in symbols)
        if unique:
            symbols = ordered_unique(symbols)
        return list(symbols)

    def primary_license_symbol(self, expression, decompose=True, **kwargs):
        """
        Return the left-most license symbol of an `expression` or None.
        `expression` is either a string or a LicenseExpression object.

        If `decompose` is True, only the left-hand license symbol of a decomposed
        LicenseWithExceptionSymbol symbol will be returned if this is the left most
        member. Otherwise a composite LicenseWithExceptionSymbol is returned in this
        case.

        Extra kwargs are passed down to the parse() function.
        """
        symbols = self.license_symbols(expression, decompose=decompose, **kwargs)
        if symbols:
            return symbols[0]

    def primary_license_key(self, expression, **kwargs):
        """
        Return the left-most license key of an `expression` or None. The underlying
        symbols are decomposed.
        `expression` is either a string or a LicenseExpression object.

        Extra kwargs are passed down to the parse() function.
       """
        prim = self.primary_license_symbol(expression, decompose=True, **kwargs)
        if prim:
            return prim.key

    def license_keys(self, expression, unique=True, **kwargs):
        """
        Return a list of licenses keys used in an expression in the same order as
        they first appear in the expression.
        `expression` is either a string or a LicenseExpression object.

        Extra kwargs are passed down to the parse() function.

        For example:
        >>> l = Licensing()
        >>> expr = ' GPL-2.0 and mit+ with blabla and mit or LGPL-2.1 and mit and mit+ with GPL-2.0'
        >>> expected = ['GPL-2.0', 'mit+', 'blabla', 'mit', 'LGPL-2.1']
        >>> assert expected == l.license_keys(l.parse(expr))
        """
        symbols = self.license_symbols(expression, unique=False, decompose=True, **kwargs)
        return self._keys(symbols, unique)

    def _keys(self, symbols, unique=True):
        keys = [ls.key for ls in symbols]
        # note: we only apply this on bare keys strings as we can have the same
        # symbol used as symbol or exception if we are not in strict mode
        if unique:
            keys = ordered_unique(keys)
        return keys

    def unknown_license_symbols(self, expression, unique=True, **kwargs):
        """
        Return a list of unknown licenses symbols used in an `expression` in the same
        order as they first appear in the `expression`.
        `expression` is either a string or a LicenseExpression object.

        Extra kwargs are passed down to the parse() function.
        """
        return [ls for ls in self.license_symbols(expression, unique=unique, decompose=True, **kwargs)
                if not ls.key in self.known_symbols]

    def unknown_license_keys(self, expression, unique=True, **kwargs):
        """
        Return a list of unknown licenses keys used in an `expression` in the same
        order as they first appear in the `expression`.

        `expression` is either a string or a LicenseExpression object.
        If a string is provided, it will be parsed.

        If `unique` is True only return unique keys.

        Extra kwargs are passed down to the parse() function.
        """
        symbols = self.unknown_license_symbols(expression, unique=False, **kwargs)
        return self._keys(symbols, unique)

    def parse(self, expression, validate=False, strict=False, simple=False, **kwargs):
        """
        Return a new license LicenseExpression object by parsing a license
        `expression` string. Check that the expression syntax is valid and raise
        an ExpressionError or an ExpressionParseError on errors.
        Return None for empty expressions.
        `expression` is either a string or a LicenseExpression object. If this
        is a LicenseExpression it is returned as-is.
        Symbols are always recognized from known symbols if `symbols` were
        provided at Licensing creation time: each license and exception is
        recognized from known license keys (and from aliases for a symbol if
        available).

        If `validate` is True and a license is unknown, an ExpressionError error
        is raised with a message listing the unknown license keys.

        If `validate` is False, no error is raised. You can call the
        `unknown_license_keys` or `unknown_license_symbols` methods to get
        unknown license keys or symbols found in a parsed LicenseExpression.

        If `strict` is True, additional exceptions will be raised if in a
        "WITH" expression such as "XXX with ZZZ" if the XXX symbol has
        `is_exception` set to True or the YYY symbol has `is_exception` set to
        False. This checks that symbols are used strictly as constructed.

        If `simple` is True, parsing will use a simple tokenizer that assumes
        that license symbols are all license keys that cannot contain spaces.

        For example:
        >>> expression = 'EPL-1.0 and Apache-1.1 OR GPL-2.0 with Classpath-exception'
        >>> parsed = Licensing().parse(expression)
        >>> expected = '(EPL-1.0 AND Apache-1.1) OR GPL-2.0 WITH Classpath-exception'
        >>> assert expected == parsed.render(template='{symbol.key}')
        """
        if expression is None:
            return

        if isinstance(expression, LicenseExpression):
            return expression

        if isinstance(expression, bytes):
            try:
                expression = str(expression)
            except:
                ext = type(expression)
                raise ExpressionError('expression must be a string and not: %(ext)r' % locals())

        if not isinstance(expression, str):
            ext = type(expression)
            raise ExpressionError('expression must be a string and not: %(ext)r' % locals())

        if not expression or not expression.strip():
            return
        try:
            # this will raise a ParseError on errors
            tokens = list(self.tokenize(expression, strict=strict, simple=simple))
            expression = super(Licensing, self).parse(tokens)
        except ParseError as e:
            new_error = ExpressionParseError(
                token_type=e.token_type, token_string=e.token_string,
                position=e.position, error_code=e.error_code)
            raise new_error

        if not isinstance(expression, LicenseExpression):
            raise ExpressionError('expression must be a LicenseExpression once parsed.')

        if validate:
            unknown_keys = self.unknown_license_keys(expression, unique=True)
            if unknown_keys:
                msg = 'Unknown license key(s): {}'.format(', '.join(unknown_keys))
                raise ExpressionError(msg)

        return expression

    def tokenize(self, expression, strict=False, simple=False):
        """
        Return an iterable of 3-tuple describing each token given an expression
        unicode string. See boolean.BooleanAlgreba.tokenize() for API details.

        This 3-tuple contains these items: (token, token string, position):
        - token: either a Symbol instance or one of TOKEN_* token types..
        - token string: the original token unicode string.
        - position: the starting index of the token string in the `expr` string.

        If `strict` is True, additional exceptions will be raised in a
        expression such as "XXX with ZZZ" if the XXX symbol has is_exception`
        set to True or the ZZZ symbol has `is_exception` set to False.

        If `simple` is True, use a simple tokenizer that assumes that license
        symbols are all license keys that cannot contain spaces.
        """
        if not expression:
            return

        if not isinstance(expression, str):
            raise ParseError(error_code=PARSE_EXPRESSION_NOT_UNICODE)

        if simple:
            tokens = self.simple_tokenizer(expression)
        else:
            advanced_tokenizer = self.get_advanced_tokenizer()
            tokens = advanced_tokenizer.tokenize(expression)

        # Assign symbol for unknown tokens
        tokens = build_symbols_from_unknown_tokens(tokens)

        # skip whitespace-only tokens
        tokens = (t for t in tokens if t.string and t.string.strip())

        # create atomic LicenseWithExceptionSymbol from WITH subexpressions
        tokens = replace_with_subexpression_by_license_symbol(tokens, strict)

        # finally yield the actual args expected by the boolean parser
        for token in tokens:
            pos = token.start
            token_string = token.string
            token_value = token.value

            if isinstance(token_value, BaseSymbol):
                token_obj = token_value
            elif isinstance(token_value, Keyword):
                token_obj = token_value.type
            else:
                raise ParseError(error_code=PARSE_INVALID_EXPRESSION)

            yield token_obj, token_string, pos

    def get_advanced_tokenizer(self):
        """
        Return an AdvancedTokenizer instance either cached or created as needed.

        If symbols were provided when this Licensing object was created, the
        tokenizer will recognize known symbol keys and aliases (ignoring case)
        when tokenizing expressions.

        A license symbol is any string separated by keywords and parens (and it
        can include spaces).
        """
        if self.advanced_tokenizer is not None:
            return self.advanced_tokenizer

        self.advanced_tokenizer = tokenizer = AdvancedTokenizer()

        add_item = tokenizer.add
        for keyword in KEYWORDS:
            add_item(keyword.value, keyword)

        # self.known_symbols has been created at Licensing initialization time and is
        # already validated and trusted here
        for key, symbol in self.known_symbols.items():
            # always use the key even if there are no aliases.
            add_item(key, symbol)
            aliases = getattr(symbol, 'aliases', [])
            for alias in aliases:
                # normalize spaces for each alias. The AdvancedTokenizer will lowercase them
                if alias:
                    alias = ' '.join(alias.split())
                    add_item(alias, symbol)

        tokenizer.make_automaton()
        return tokenizer

    def advanced_tokenizer(self, expression):
        """
        Return an iterable of Token describing each token given an expression
        unicode string.
        """
        tokenizer = self.get_advanced_tokenizer()
        return tokenizer.tokenize(expression)

    def simple_tokenizer(self, expression):
        """
        Return an iterable of Token describing each token given an expression
        unicode string.

        The split is done on spaces, keywords and parens. Anything else is a
        symbol token, e.g. a typically license key or license id (that contains
        no spaces or parens).

        If symbols were provided when this Licensing object was created, the
        tokenizer will recognize known symbol keys (ignoring case) when
        tokenizing expressions.
        """

        symbols = self.known_symbols_lowercase or {}

        for match in _simple_tokenizer(expression):
            if not match:
                continue
            # set start and end as string indexes
            start, end = match.span()
            end = end - 1
            match_getter = match.groupdict().get

            space = match_getter('space')
            if space:
                yield Token(start, end, space, None)

            lpar = match_getter('lpar')
            if lpar:
                yield Token(start, end, lpar, KW_LPAR)

            rpar = match_getter('rpar')
            if rpar:
                yield Token(start, end, rpar, KW_RPAR)

            sym_or_op = match_getter('symop')
            if sym_or_op:
                sym_or_op_lower = sym_or_op.lower()

                operator = OPERATORS.get(sym_or_op_lower)
                if operator:
                    yield Token(start, end, sym_or_op, operator)
                else:
                    sym = symbols.get(sym_or_op_lower)
                    if not sym:
                        sym = LicenseSymbol(key=sym_or_op)
                    yield Token(start, end, sym_or_op, sym)


def build_symbols_from_unknown_tokens(tokens):
    """
    Yield Token given a sequence of Token replacing unmatched contiguous Tokens
    by a single token with a LicenseSymbol.
    """
    tokens = list(tokens)

    unmatched = deque()

    def build_token_with_symbol():
        """
        Build and return a new Token from accumulated unmatched tokens or None.
        """
        if not unmatched:
            return
        # strip trailing spaces
        trailing_spaces = []
        while unmatched and not unmatched[-1].string.strip():
            trailing_spaces.append(unmatched.pop())

        if unmatched:
            string = ' '.join(t.string for t in unmatched if t.string.strip())
            start = unmatched[0].start
            end = unmatched[-1].end
            toksym = LicenseSymbol(string)
            unmatched.clear()
            yield Token(start, end, string, toksym)

        for ts in trailing_spaces:
            yield ts

    for tok in tokens:
        if tok.value:
            for symtok in build_token_with_symbol():
                yield symtok
            yield tok
        else:
            if not unmatched and not tok.string.strip():
                # skip leading spaces
                yield tok
            else:
                unmatched.append(tok)

    # end remainders
    for symtok in build_token_with_symbol():
        yield symtok


def build_token_groups_for_with_subexpression(tokens):
    """
    Yield tuples of Token given a sequence of Token such that:
     - all symbol-with-symbol sequences of 3 tokens are grouped in a three-tuple
     - other tokens are a single token wrapped in a tuple.
    """

    # if n-1 is sym, n is with and n+1 is sym: yield this as a group for a with
    # exp otherwise: yield each single token as a group

    tokens = list(tokens)

    # check three contiguous tokens that may form "lic WITh exception" sequence
    triple_len = 3

    # shortcut if there are no grouping possible
    if len(tokens) < triple_len:
        for tok in tokens:
            yield (tok,)
        return

    # accumulate three contiguous tokens
    triple = deque()
    triple_popleft = triple.popleft
    triple_clear = triple.clear
    tripple_append = triple.append

    for tok in tokens:
        if len(triple) == triple_len:
            if is_with_subexpression(triple):
                yield tuple(triple)
                triple_clear()
            else:
                prev_tok = triple_popleft()
                yield (prev_tok,)
        tripple_append(tok)

    # end remainders
    if triple:
        if len(triple) == triple_len and is_with_subexpression(triple):
            yield tuple(triple)
        else:
            for tok in triple:
                yield (tok,)


def is_with_subexpression(tokens_tripple):
    """
    Return True if a Token tripple is a WITH license sub-expression.
    """
    lic, wit, exc = tokens_tripple
    return (isinstance(lic.value, LicenseSymbol)
        and wit.value == KW_WITH
        and isinstance(exc.value, LicenseSymbol)
    )


def replace_with_subexpression_by_license_symbol(tokens, strict=False):
    """
    Given an iterable of Token, yiled token, replacing any XXX WITH ZZZ
    subexpression by a LicenseWithExceptionSymbol symbol.

    Check validity of with subexpessions and raise ParseError as needed.

    If `strict` is True also raise ParseError if the left hand side
    LicenseSymbol has is_exception True or if the right hand side
    LicenseSymbol has is_exception False.
    """
    token_groups = build_token_groups_for_with_subexpression(tokens)

    for token_group in token_groups:
        len_group = len(token_group)

        if not len_group:
            # This should never happen
            continue

        if len_group == 1:
            # a single token
            token = token_group[0]
            tval = token.value

            if isinstance(tval, Keyword):
                if tval.type == TOKEN_WITH:
                    # keyword
                    # a single group cannot be a single 'WITH' keyword:
                    # this is an error that we catch and raise here.
                    raise ParseError(
                        token_type=TOKEN_WITH, token_string=token.string,
                        position=token.start, error_code=PARSE_INVALID_EXPRESSION)

            elif isinstance(tval, LicenseSymbol):
                if strict and tval.is_exception:
                    raise ParseError(
                        token_type=TOKEN_SYMBOL, token_string=token.string,
                        position=token.start, error_code=PARSE_INVALID_EXCEPTION)

            else:
                # this should not be possible by design
                raise Exception('Licensing.tokenize is internally confused...:' + repr(tval))

            yield token
            continue

        if len_group != 3:
            # this should never happen
            string = ' '.join([tok.string for tok in token_group])
            start = token_group[0].start
            raise ParseError(
                TOKEN_SYMBOL, string, start, PARSE_INVALID_EXPRESSION)

        # from now on we have a tripple of tokens: a WITH sub-expression such as "A with
        # B" seq of three tokens
        lic_token, WITH , exc_token = token_group

        token_string = ' '.join([
            lic_token.string,
            WITH.string.strip(),
            exc_token.string
        ])

        # the left hand side license symbol
        lic_sym = lic_token.value

        # this should not happen
        if not isinstance(lic_sym, LicenseSymbol):
            raise ParseError(
                TOKEN_SYMBOL, lic_token.string, lic_token.start,
                PARSE_INVALID_SYMBOL)

        if strict and lic_sym.is_exception:
            raise ParseError(
                TOKEN_SYMBOL, lic_token.string, lic_token.start,
                PARSE_INVALID_EXCEPTION)

        # the right hand side exception symbol
        exc_sym = exc_token.value

        if not isinstance(exc_sym, LicenseSymbol):
            raise ParseError(
                TOKEN_SYMBOL, lic_sym.string, lic_sym.start,
                PARSE_INVALID_SYMBOL)

        if strict and not exc_sym.is_exception:
            raise ParseError(
                TOKEN_SYMBOL, exc_token.string, exc_token.start,
                PARSE_INVALID_SYMBOL_AS_EXCEPTION)

        lic_exc_sym = LicenseWithExceptionSymbol(lic_sym, exc_sym, strict)

        token = Token(
            lic_token.start,
            exc_token.end,
            token_string,
            lic_exc_sym,
        )
        yield token


class Renderable(object):
    """
    An interface for renderable objects.
    """

    def render(self, template='{symbol.key}', *args, **kwargs):
        """
        Return a formatted string rendering for this expression using the `template`
        format string to render each symbol. The variable available are `symbol.key`
        and any other attribute that was attached to a license symbol instance and a
        custom template can be provided to handle custom HTML rendering or similar.

        For symbols that hold multiple licenses (e.g. a WITH statement) the template
        is applied to each symbol individually.

        Note that when render() is called the *args and **kwargs are propagated
        recursively to any Renderable object render() method.
        """
        return NotImplementedError

    def render_as_readable(self, template='{symbol.key}', *args, **kwargs):
        """
        Return a formatted string rendering for this expression using the
        `template` format string to render each symbol.  Add extra parenthesis
        around WITH sub-expressions for improved readbility. See `render()` for
        other arguments.
        """
        if isinstance(self, LicenseWithExceptionSymbol):
            return self.render(
                template=template, wrap_with_in_parens=False, *args, **kwargs)
        else:
            return self.render(template=template, wrap_with_in_parens=True, *args, **kwargs)


class BaseSymbol(Renderable, boolean.Symbol):
    """
    A base class for all symbols.
    """

    def decompose(self):
        """
        Yield the underlying symbols of this symbol.
        """
        raise NotImplementedError

    def __contains__(self, other):
        """
        Test if expr is contained in this symbol.
        """
        if not isinstance(other, BaseSymbol):
            return False
        if self == other:
            return True

        return any(mine == other for mine in self.decompose())


# validate license keys
is_valid_license_key = re.compile(r'^[-:\w\s\.\+]+$', re.UNICODE).match


# TODO: we need to implement comparison by hand instead
@total_ordering
class LicenseSymbol(BaseSymbol):
    """
    A LicenseSymbol represents a license as used in a license expression.
    """

    def __init__(self, key, aliases=tuple(), is_exception=False, *args, **kwargs):
        if not key:
            raise ExpressionError(
                'A license key cannot be empty: %(key)r' % locals())

        if not isinstance(key, str):
            if isinstance(key, bytes):
                try:
                    key = str(key)
                except:
                    raise ExpressionError(
                        'A license key must be a unicode string: %(key)r' % locals())
            else:
                raise ExpressionError(
                    'A license key must be a unicode string: %(key)r' % locals())

        key = key.strip()

        if not key:
            raise ExpressionError(
                'A license key cannot be blank: "%(key)s"' % locals())

        # note: key can contain spaces
        if not is_valid_license_key(key):
            raise ExpressionError(
                'Invalid license key: the valid characters are: letters and numbers, '
                'underscore, dot, colon or hyphen signs and spaces: "%(key)s"' % locals())

        # normalize for spaces
        key = ' '.join(key.split())

        if key.lower() in KEYWORDS_STRINGS:
            raise ExpressionError(
                'Invalid license key: a key cannot be a reserved keyword: "or",'
                ' "and" or "with: "%(key)s"' % locals())

        self.key = key

        if aliases and not isinstance(aliases, (list, tuple,)):
            raise TypeError('License aliases must be a sequence.')
        self.aliases = aliases and tuple(aliases) or tuple()
        self.is_exception = is_exception

        # super only know about a single "obj" object.
        super(LicenseSymbol, self).__init__(self.key)

    def decompose(self):
        """
        Return an iterable of the underlying symbols for this symbol.
        """
        yield self

    def __hash__(self, *args, **kwargs):
        return hash((self.key, self.is_exception))

    def __eq__(self, other):
        if self is other:
            return True
        if not (isinstance(other, self.__class__) or self.symbol_like(other)):
            return False
        return self.key == other.key and self.is_exception == other.is_exception

    def __ne__(self, other):
        if self is other:
            return False
        if not (isinstance(other, self.__class__) or self.symbol_like(other)):
            return True
        return (self.key != other.key or self.is_exception != other.is_exception)

    def __lt__(self, other):
        if isinstance(
            other, (LicenseSymbol, LicenseWithExceptionSymbol, LicenseSymbolLike)):
            return str(self) < str(other)
        else:
            return NotImplemented

    __nonzero__ = __bool__ = lambda s: True

    def render(self, template='{symbol.key}', *args, **kwargs):
        return template.format(symbol=self)

    def __str__(self):
        return self.key

    def __len__(self):
        return len(self.key)

    def __repr__(self):
        cls = self.__class__.__name__
        key = self.key
        aliases = self.aliases and ('aliases=%(a)r, ' % {'a': self.aliases}) or ''
        is_exception = self.is_exception
        return '%(cls)s(%(key)r, %(aliases)sis_exception=%(is_exception)r)' % locals()

    def __copy__(self):
        return LicenseSymbol(self.key, tuple(self.aliases), self.is_exception)

    @classmethod
    def symbol_like(cls, symbol):
        """
        Return True if `symbol` is a symbol-like object with its essential attributes.
        """
        return hasattr(symbol, 'key') and hasattr(symbol, 'is_exception')


# TODO: we need to implement comparison by hand instead
@total_ordering
class LicenseSymbolLike(LicenseSymbol):
    """
    A LicenseSymbolLike object wraps a symbol-like object to expose a
    LicenseSymbol behavior.
    """

    def __init__(self, symbol_like, *args, **kwargs):
        if not self.symbol_like(symbol_like):
            raise ExpressionError(
                'Not a symbol-like object: %(symbol_like)r' % locals())

        self.wrapped = symbol_like
        super(LicenseSymbolLike, self).__init__(self.wrapped.key, *args, **kwargs)

        self.is_exception = self.wrapped.is_exception
        self.aliases = getattr(self.wrapped, 'aliases', tuple())

        # can we delegate rendering to a render method of the wrapped object?
        # we can if we have a .render() callable on the wrapped object.
        self._render = None
        renderer = getattr(symbol_like, 'render', None)
        if callable(renderer):
            self._render = renderer

    def __copy__(self):
        return LicenseSymbolLike(symbol_like=self.wrapped)

    def render(self, template='{symbol.key}', *args, **kwargs):
        if self._render:
            return self._render(template, *args, **kwargs)
        return super(LicenseSymbolLike, self).render(template, *args, **kwargs)

    __nonzero__ = __bool__ = lambda s: True

    def __hash__(self, *args, **kwargs):
        return hash((self.key, self.is_exception))

    def __eq__(self, other):
        if self is other:
            return True
        if not (isinstance(other, self.__class__) or self.symbol_like(other)):
            return False
        return self.key == other.key and self.is_exception == other.is_exception

    def __ne__(self, other):
        if self is other:
            return False
        if not (isinstance(other, self.__class__) or self.symbol_like(other)):
            return True
        return (self.key != other.key or self.is_exception != other.is_exception)

    def __lt__(self, other):
        if isinstance(
            other, (LicenseSymbol, LicenseWithExceptionSymbol, LicenseSymbolLike)):
            return str(self) < str(other)
        else:
            return NotImplemented


# TODO: we need to implement comparison by hand instead
@total_ordering
class LicenseWithExceptionSymbol(BaseSymbol):
    """
    A LicenseWithExceptionSymbol represents a license "with" an exception as used in
    a license expression. It holds two LicenseSymbols objects: one for the left-hand
    license proper and one for the right-hand exception to this license and deals
    with the specifics of resolution, validation and representation.
    """

    def __init__(self, license_symbol, exception_symbol, strict=False, *args, **kwargs):
        """
        Initialize a new LicenseWithExceptionSymbol from a `license_symbol` and a
        `exception_symbol` symbol-like objects.

        Raise a ExpressionError exception if strict is True and either:
        - license_symbol.is_exception is True
        - exception_symbol.is_exception is not True
        """
        if not LicenseSymbol.symbol_like(license_symbol):
            raise ExpressionError(
                'license_symbol must be a LicenseSymbol-like object: %(license_symbol)r' % locals())

        if strict and license_symbol.is_exception:
            raise ExpressionError(
                'license_symbol cannot be an exception with "is_exception" set to True: %(license_symbol)r' % locals())

        if not LicenseSymbol.symbol_like(exception_symbol):
            raise ExpressionError(
                'exception_symbol must be a LicenseSymbol-like object: %(exception_symbol)r' % locals())

        if strict and not exception_symbol.is_exception:
            raise ExpressionError(
                'exception_symbol must be an exception with "is_exception" set to True: %(exception_symbol)r' % locals())

        self.license_symbol = license_symbol
        self.exception_symbol = exception_symbol

        super(LicenseWithExceptionSymbol, self).__init__(str(self))

    def __copy__(self):
        return LicenseWithExceptionSymbol(copy(self.license_symbol), copy(self.exception_symbol))

    def decompose(self):
        yield self.license_symbol
        yield self.exception_symbol

    def render(self, template='{symbol.key}', wrap_with_in_parens=False, *args, **kwargs):
        """
        Return a formatted WITH expression. If `wrap_with_in_parens`, wrap in
        parens a WITH expression, unless it is alone and not used with other AND
        or OR sub-expressions.
        """
        lic = self.license_symbol.render(template, *args, **kwargs)
        exc = self.exception_symbol.render(template, *args, **kwargs)
        if wrap_with_in_parens:
            temp = '(%(lic)s WITH %(exc)s)'
        else:
            temp = '%(lic)s WITH %(exc)s'
        return temp % locals()

    def __hash__(self, *args, **kwargs):
        return hash((self.license_symbol, self.exception_symbol,))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            return False
        return (self.license_symbol == other.license_symbol
            and self.exception_symbol == other.exception_symbol)

    def __ne__(self, other):
        if self is other:
            return False
        if not isinstance(other, self.__class__):
            return True
        return not (self.license_symbol == other.license_symbol
            and self.exception_symbol == other.exception_symbol)

    def __lt__(self, other):
        if isinstance(
            other, (LicenseSymbol, LicenseWithExceptionSymbol, LicenseSymbolLike)):
            return str(self) < str(other)
        else:
            return NotImplemented

    __nonzero__ = __bool__ = lambda s: True

    def __str__(self):
        lkey = self.license_symbol.key
        ekey = self.exception_symbol.key
        return '%(lkey)s WITH %(ekey)s' % locals()

    def __repr__(self):
        data = dict(cls=self.__class__.__name__)
        data.update(self.__dict__)
        return '%(cls)s(license_symbol=%(license_symbol)r, exception_symbol=%(exception_symbol)r)' % data


class RenderableFunction(Renderable):
    # derived from the __str__ code in boolean.py

    def render(self, template='{symbol.key}', *args, **kwargs):
        """
        Render an expression as a string, recursively applying the string `template`
        to every symbols and operators.
        """
        expression_args = self.args
        if len(expression_args) == 1:
            # a bare symbol
            sym = expression_args[0]
            if isinstance(sym, Renderable):
                sym = sym.render(template, *args, **kwargs)

            else:
                print('WARNING: symbol is not renderable: using plain string representation.')
                # FIXME: CAN THIS REALLY HAPPEN since we only have symbols, OR, AND?
                sym = str(sym)

            if self.isliteral:
                rendered = '%s%s' % (self.operator, sym)
            else:
                # NB: the operator str already has a leading and trailing space
                rendered = '%s(%s)' % (self.operator, sym)
            return rendered

        rendered_items = []
        rendered_items_append = rendered_items.append
        for arg in expression_args:
            if isinstance(arg, Renderable):
                # recurse
                rendered = arg.render(template, *args, **kwargs)

            else:
                print('WARNING: object in expression is not renderable: falling back to plain string representation: %(arg)r.')
                # FIXME: CAN THIS REALLY HAPPEN since we only have symbols, or and AND?
                rendered = str(arg)

            if arg.isliteral:
                rendered_items_append(rendered)
            else:
                rendered_items_append('(%s)' % rendered)

        return self.operator.join(rendered_items)


class AND(RenderableFunction, boolean.AND):
    """
    Custom representation for the AND operator to uppercase.
    """

    def __init__(self, *args):
        if len(args) < 2:
            raise ExpressionError('AND requires two or more licenses as in: MIT AND BSD')
        super(AND, self).__init__(*args)
        self.operator = ' AND '


class OR(RenderableFunction, boolean.OR):
    """
    Custom representation for the OR operator to uppercase.
    """

    def __init__(self, *args):
        if len(args) < 2:
            raise ExpressionError('OR requires two or more licenses as in: MIT OR BSD')
        super(OR, self).__init__(*args)
        self.operator = ' OR '


def ordered_unique(seq):
    """
    Return unique items in a sequence seq preserving the original order.
    """
    if not seq:
        return []
    uniques = []
    for item in seq:
        if item in uniques:
            continue
        uniques.append(item)
    return uniques


def as_symbols(symbols):
    """
    Return an iterable of LicenseSymbol objects from a sequence of `symbols` or
    strings. If an item is a string, then create a new LicenseSymbol for it
    using the string as key. If this is not a string it must be a LicenseSymbol-
    like type. It will raise a TypeError expection if an item is neither a
    string or LicenseSymbol- like.
    """
    if symbols:
        for symbol in symbols:
            if not symbol:
                continue
            if isinstance(symbol, bytes):
                try:
                    symbol = str(symbol)
                except:
                    raise TypeError('%(symbol)r is not a unicode string.' % locals())

            if isinstance(symbol, str):
                if symbol.strip():
                    yield LicenseSymbol(symbol)

            elif isinstance(symbol, LicenseSymbol):
                yield symbol

            elif LicenseSymbol.symbol_like(symbol):
                yield LicenseSymbolLike(symbol)

            else:
                raise TypeError('%(symbol)r is not a unicode string '
                                'or a LicenseSymbol-like instance.' % locals())


def validate_symbols(symbols, validate_keys=False):
    """
    Return a tuple of (`warnings`, `errors`) given a sequence of `symbols`
    LicenseSymbol-like objects.

    - warnings is a list of validation warnings messages (possibly empty if there
      were no warnings).
    - errors is a list of validation error messages (possibly empty if there were no
      errors).

    Keys and aliases are cleaned and validated for uniqueness.
    """

    # collection used for checking unicity and correctness
    seen_keys = set()
    seen_aliases = {}
    seen_exceptions = set()

    # collections to accumulate invalid data and build error messages at the end
    not_symbol_classes = []
    dupe_keys = set()
    dupe_exceptions = set()
    dupe_aliases = defaultdict(list)
    invalid_keys_as_kw = set()
    invalid_alias_as_kw = defaultdict(list)

    # warning
    warning_dupe_aliases = set()

    for symbol in symbols:
        if not isinstance(symbol, LicenseSymbol):
            not_symbol_classes.append(symbol)
            continue

        key = symbol.key
        key = key.strip()
        keyl = key.lower()

        # ensure keys are unique
        if keyl in seen_keys:
            dupe_keys.add(key)

        # key cannot be an expression keyword
        if keyl in KEYWORDS_STRINGS:
            invalid_keys_as_kw.add(key)

        # keep a set of unique seen keys
        seen_keys.add(keyl)

        # aliases is an optional attribute
        aliases = getattr(symbol, 'aliases', [])
        initial_alias_len = len(aliases)

        # always normalize aliases for spaces and case
        aliases = set([' '.join(alias.lower().strip().split()) for alias in aliases])

        # KEEP UNIQUES, remove empties
        aliases = set(a for a in aliases if a)

        # issue a warning when there are duplicated or empty aliases
        if len(aliases) != initial_alias_len:
            warning_dupe_aliases.add(key)

        # always add a lowercase key as an alias
        aliases.add(keyl)

        for alias in aliases:
            # note that we do not treat as an error the presence of a duplicated
            # alias pointing to the same key

            # ensure that a possibly duplicated alias does not point to another key
            aliased_key = seen_aliases.get(alias)
            if aliased_key and aliased_key != keyl:
                dupe_aliases[alias].append(key)

            # an alias cannot be an expression keyword
            if alias in KEYWORDS_STRINGS:
                invalid_alias_as_kw[key].append(alias)

            seen_aliases[alias] = keyl

        if symbol.is_exception:
            if keyl in seen_exceptions:
                dupe_exceptions.add(keyl)
            else:
                seen_exceptions.add(keyl)

    # build warning and error messages from invalid data
    errors = []
    for ind in sorted(not_symbol_classes):
        errors.append('Invalid item: not a LicenseSymbol object: %(ind)s.' % locals())

    for dupe in sorted(dupe_keys):
        errors.append('Invalid duplicated license key: %(dupe)s.' % locals())

    for dalias, dkeys in sorted(dupe_aliases.items()):
        dkeys = ', '.join(dkeys)
        errors.append('Invalid duplicated alias pointing to multiple keys: '
                      '%(dalias)s point to keys: %(dkeys)s.' % locals())

    for ikey, ialiases in sorted(invalid_alias_as_kw.items()):
        ialiases = ', '.join(ialiases)
        errors.append('Invalid aliases: an alias cannot be an expression keyword. '
                      'key: "%(ikey)s", aliases: %(ialiases)s.' % locals())

    for dupe in sorted(dupe_exceptions):
        errors.append('Invalid duplicated license exception key: %(dupe)s.' % locals())

    for ikw in sorted(invalid_keys_as_kw):
        errors.append('Invalid key: a key cannot be an expression keyword: %(ikw)s.' % locals())

    warnings = []
    for dupeal in sorted(dupe_aliases):
        errors.append('Duplicated or empty aliases ignored for license key: %(dupeal)r.' % locals())

    return warnings, errors
