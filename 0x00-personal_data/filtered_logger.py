#!/usr/bin/env python3
"""
A Log Filtering Module
"""

import re
import logging
from typing import List


with open("user_data.csv") as f:
    piis = f.readline()[:-1]  # remove newline char
piis = piis.split(',')
piis.pop(4)
piis.pop(5)
piis.pop(5)
PII_FIELDS = tuple(piis)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization function
        Example:
        formatter = RedactingFormatter(fields=["email", "ssn", "password"])
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats code based on the FORMAT"""
        x = super().format(record).split()
        msg = filter_datum(self.fields, self.REDACTION, x[5], self.SEPARATOR)
        x.pop(5)
        return ' '.join(x + re.split(r'(?<=;)(?=\w+=)', msg))


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """This filters the log message using a RegEx"""
    for field in fields:
        p = (rf'({re.escape(field)}=)'
             rf'[^{re.escape(separator)})]+'
             rf'({re.escape(separator)})')
        message = re.sub(p, rf'\1{redaction}\2', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a new Logger instance """
    logger = logging.Logger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()  # handler
    handler.setFormatter(RedactingFormatter(PII_FIELDS))  # formatter

    logger.addHandler(handler)  # add handler to logger
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a mySQL connector object"""
    
