#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A Python module that emulates shell commands."""

# IMPORT STANDARD LIBRARIES
import os


def which(program):
    """Try to find where a shell command is defined, using the user's environment.

    Args:
        program (str): The executable to look for. e.g. "less".

    Returns:
        str: The found path on-disk where `program` was found. e.g. "/usr/bin/less".

    """
    # Reference: https://stackoverflow.com/a/377028/3626104
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return ''
