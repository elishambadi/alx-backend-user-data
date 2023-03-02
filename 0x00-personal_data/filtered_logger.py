#!/usr/bin/env python3
"""A Log Filtering Module
"""
import re


def filter_datum(fields: list, redaction: str, message: str, separator: chr):
    """This filters the log message using a RegEx
    """
    x = message
    for i in range(len(fields)):
        password_regex = rf'({re.escape(fields[i])}=)[^;]+(;)'
        x = re.sub(password_regex, r'\1xxx\2', x)
    return x
