#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A basic module that is used to find paths with `@` quotes.

This module is used to extend Vim's `:normal gf` mapping for USD files.

"""

# IMPORT STANDARD LIBRARIES
import itertools
import subprocess

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from . import shell_helper

REGISTERED_RESOLVERS = []


def _resolve_using_usd(path):
    """str: Try to resolve `path` using Pixar's Python API."""
    try:
        from pxr import Ar
    except ImportError:
        return ""

    return Ar.GetResolver().Resolve(path)


def _resolve_with_subprocess(path):
    """str: Try to use the commandline `usdresolve` executable to resolve `path`."""
    if not shell_helper.which("usdresolve"):
        return ""

    command = ['usdresolve', path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error) = process.communicate()

    if process.returncode:  # If the return code is not 0, then it errored
        return ""

    if error:
        return ""

    return output.rstrip()


def register_resolver(resolver):
    """Add the given function as a resolver open when looking up USD paths.

    Args:
        resolver (callable[str] -> str):
            A function that resolves a USD Asset path into a file
            on-disk. This function cannot raise an exceptions. If the
            path doesn't exist then `resolver` should return an empty
            string.

    Raises:
        ValueError: If `resolver` will not work with this plugin.

    """
    if not callable(resolver):
        raise ValueError('resolver "{resolver}" must be a callable function.'
                         ''.format(resolver=resolver))

    REGISTERED_RESOLVERS.append(resolver)


def resolve(path):
    """str: Find the path on-disk that `path` represents, if possible.

    Args:
        path (str):
            Some USD Asset path to resolve.
            It could be a file path or some USD-compatible URI.

    Returns:
        str: The resolve path on-disk, if it could be found.

    """
    for resolver in itertools.chain(
        [_resolve_using_usd, _resolve_with_subprocess],
        REGISTERED_RESOLVERS,
    ):
        resolved_path = resolver(path)
        if resolved_path:
            return resolved_path

    return ""
