#!/usr/bin/env python3
"""PII Filtered Logging"""
import re


def filter_datum(fields, redaction, msg, sep):
    """Filters a log message for PII and redacts it"""
    for field in fields:
        msg = re.sub(fr"({field}={sep}?)[^;]+", fr"\1{redaction}", msg)
    return msg
