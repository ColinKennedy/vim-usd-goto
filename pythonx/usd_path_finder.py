#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A basic module that is used to find paths with `@` quotes.

This module basically replaces Vim's `:normal gf` command.

"""

# IMPORT STANDARD LIBRARIES
import logging
import os
import re
import subprocess

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
import rez_helper
import shell_helper

_ASSET_IDENTIFIER = re.compile(r"@(?P<path>[^@]+)@")


def _eval(key, default=None):
    try:
        return vim.eval(key)
    except Exception:
        return default


def _resolve_with_subprocess(path):
    """str: Try to use `usdresolve` to resolve the path."""

    def _get_resolve_base_command():
        if shell_helper.which("usdresolve"):
            return ["usdresolve"]

        packages = (_eval("g:usd_rez_package", default="USD"),)
        package = rez_helper.package_chooser(packages)
        if not package:
            return []

        # Try to use Rez to get a shell which has the `usdresolve` executable
        return ["rez-env", package, "--", "usdresolve"]

    base = _get_resolve_base_command()
    if not base:
        return ""

    command = base + [path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error) = process.communicate()

    if process.returncode:  # If the return code is not 0, then it errored
        return ""

    if error:
        return ""

    return output.rstrip()


def find_selection():
    """str: Find the closest path in `@` quotes, if any can be found."""
    row, column = vim.current.window.cursor
    row -= 1  # Subtract a row to get the current row's index
    line = vim.current.buffer[row]

    for match in _ASSET_IDENTIFIER.finditer(line):
        if match.start(0) <= column and match.end(0) >= column:
            return match.group("path")

    return ""


def get_visual_selection():
    """str: Get the user's visual selection, if any."""
    start = vim.current.buffer.mark("<")

    if start is None:
        return ""

    end = vim.current.buffer.mark(">")

    if end is None:
        return ""

    start_row, start_column = start
    end_row, end_column = end
    start_row -= 1
    end_row -= 1

    characters = []
    for row in range(start_row, end_row + 1):
        line = vim.current.buffer[row]

        if row == start_row and row == end_row:
            line = line[start_column : end_column + 1]
        elif row == start_row:
            line = line[start_column:]
        elif row == end_row:
            line = line[: end_column + 1]

        characters.append(line)

    return "\n".join(characters)


def get_selected_path(visual_mode):
    """Find the path that is under the cursor (using visual mode or by guessing).

    If the user is not in visual mode, find the nearest text in wrapped
    in `@` characters and use that, instead.

    Returns:
        str: The found path, if any.

    """
    try:
        from pxr import Ar

        _resolve = Ar.GetResolver().Resolve
    except ImportError:
        _resolve = _resolve_with_subprocess

    selection = ""
    if visual_mode:
        selection = get_visual_selection()

    if not selection:
        selection = find_selection()

    if not selection:
        return ""

    if os.path.isabs(selection):
        return selection
    else:
        # Resolve a relative path into an absolute path, if needed
        current_directory = vim.eval('expand("%:p:h")')
        selection = os.path.normpath(os.path.join(current_directory, selection))

    # Change a USD path URI into a file-path, if needed
    selection = _resolve(selection)

    return selection
