#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A basic module that is used to find paths with `@` quotes.

This module basically replaces Vim's `:normal gf` command.

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
    try:
        from pxr import Ar
    except ImportError:
        return ""

    return Ar.GetResolver().Resolve(path)


def _resolve_with_subprocess(path):
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
    if not callable(resolver):
        raise ValueError('resolver "{resolver}" must be a callable function.'
                         ''.format(resolver=resolver))

    REGISTERED_RESOLVERS.append(resolver)


def resolve(path):
    for resolver in itertools.chain(
        [_resolve_using_usd, _resolve_with_subprocess],
        REGISTERED_RESOLVERS,
    ):
        resolved_path = resolver(path)
        if resolved_path:
            return resolved_path

    return ""
