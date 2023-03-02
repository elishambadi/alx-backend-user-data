#!/usr/bin/env python3
"""A Log Filtering Module
"""
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        x = super().format(record).split()
        msg = filter_datum(self.fields, self.REDACTION, x[5], self.SEPARATOR)
        x.pop(5)
        x = x + re.split(r'(?<=;)(?=\w+=)', msg)
        return ' '.join(x)


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    """This filters the log message using a RegEx
    """
    #  print("{} {} {} {}".format(fields, redaction, message, separator))
    for i in range(len(fields)):
        p = (rf'({re.escape(fields[i])}=)'
             rf'[^{re.escape(separator)})]+'
             rf'({re.escape(separator)})')
        message = re.sub(p, rf'\1{redaction}\2', message)
    return message
