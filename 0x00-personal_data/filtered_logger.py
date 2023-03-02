#!/usr/bin/env python3
"""A Log Filtering Module
"""
import re


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    """This filters the log message using a RegEx
    """
    for i in range(len(fields)):
        p = (rf'({re.escape(fields[i])}=)'
             rf'[^{re.escape(separator)})]+'
             rf'({re.escape(separator)})')
        message = re.sub(p, r'\1xxx\2', message)
    return message
