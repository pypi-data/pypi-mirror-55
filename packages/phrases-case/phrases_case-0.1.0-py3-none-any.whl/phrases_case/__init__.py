u"""Convert phrases between different cases.  """

from __future__ import absolute_import
__version__ = u'0.1.0'

import re


def snake(v, **_3to2kwargs):
    if 'seperator' in _3to2kwargs: seperator = _3to2kwargs['seperator']; del _3to2kwargs['seperator']
    else: seperator = u'_'
    u"""Convert phrases case to snake case.

    Args:
        v (str): Phrases to convert.
        seperator (str, optional): phrase seperator. Defaults to '_'.

    Returns:
        str: Converted Phrases.

    >>> snake('space case')
    'space_case'
    >>> snake('snake_case')
    'snake_case'
    >>> snake('hyphen-case')
    'hyphen_case'
    >>> snake('camelCase')
    'camel_case'
    >>> snake('PascalCase')
    'pascal_case'
    """
    return seperator.join([i.lower() for i in re.split(u'(?=[A-Z])|[ \\-_]', v) if i])


def pascal(v):
    u"""Convert text to pascal case.

    Args:
        v (str): Phrases to convert.

    Returns:
        str: Converted Phrases.

    >>> pascal('space case')
    'SpaceCase'
    >>> pascal('snake_case')
    'SnakeCase'
    >>> pascal('hyphen-case')
    'HyphenCase'
    >>> pascal('camelCase')
    'CamelCase'
    >>> pascal('PascalCase')
    'PascalCase'
    """

    return u''.join(x[0].title() + x[1:] for x in re.split(u'[\\-_ ]', v))


def camel(v):
    u"""Convert text to camel case.

    Args:
        v (str): Phrases to convert.

    Returns:
        str: Converted Phrases.

    >>> camel('space case')
    'spaceCase'
    >>> camel('snake_case')
    'snakeCase'
    >>> camel('hyphen-case')
    'hyphenCase'
    >>> camel('camelCase')
    'camelCase'
    >>> camel('PascalCase')
    'pascalCase'
    """

    ret = pascal(v)
    if ret:
        ret = ret[0].lower() + ret[1:]
    return ret


def space(v):
    u"""Shortcut for snake(v, seperator=' ')

    Args:
        v (str): Phrases to convert.

    Returns:
        str: Converted Phrases.

    >>> space('space case')
    'space case'
    >>> space('snake_case')
    'snake case'
    >>> space('hyphen-case')
    'hyphen case'
    >>> space('camelCase')
    'camel case'
    >>> space('PascalCase')
    'pascal case'
    """
    return snake(v, seperator=u' ')


def hyphen(v):
    u"""Shortcut for snake(v, seperator='-')

    Args:
        v (str): Phrases to convert.

    Returns:
        str: Converted Phrases.

    >>> hyphen('space case')
    'space-case'
    >>> hyphen('snake_case')
    'snake-case'
    >>> hyphen('hyphen-case')
    'hyphen-case'
    >>> hyphen('camelCase')
    'camel-case'
    >>> hyphen('PascalCase')
    'pascal-case'
    """
    return snake(v, seperator=u'-')
