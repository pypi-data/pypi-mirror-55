# -*- coding: utf-8 -*-
"""Utility functions."""

import json

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import JsonLexer


def get_from_json_or_default(json, path, default_value):
    """Try to load a key breadcrumb from a JSON object or return default."""
    if not path:
        return default_value
    json = json if json else {}
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        return json if json else default_value
    except KeyError:
        return default_value


def beautify_json_string(json_string, colorize=False, sort_keys=False):
    """Beautify JSON string with optional coloring."""
    return beautify_json(json.loads(json_string), colorize, sort_keys)


def beautify_json(json_obj, colorize=False, sort_keys=False):
    """Beautify JSON with optional coloring."""
    formatted_json = json.dumps(json_obj, sort_keys=sort_keys, indent=4)
    if not colorize:
        return formatted_json
    return highlight(formatted_json, JsonLexer(), TerminalFormatter())


def truncate_with_ellipsis(string, length):
    """Truncate a string at the given length or return it."""
    string = string if string else ''
    return (string[:length] + '..') if len(string) > length else string


def remove_common_prefix_from_string_list(string_list):
    """If a list of strings share the same prefix they will be removed."""
    if any([len(string) < 2 or not string for string in string_list]):
        return string_list
    uniq_first_char = len(set([string[:1] for string in string_list]))
    if uniq_first_char == 1:
        string_list = remove_common_prefix_from_string_list(
            [string[1:] for string in string_list])
    return string_list


def remove_common_suffix_from_string_list(string_list):
    """If a list of strings share the same suffix they will be removed."""
    if any([len(string) < 2 or not string for string in string_list]):
        return string_list
    uniq_last_char = len(set([string[-1:] for string in string_list]))
    if uniq_last_char == 1:
        string_list = remove_common_suffix_from_string_list(
            [string[:-1] for string in string_list])
    return string_list
