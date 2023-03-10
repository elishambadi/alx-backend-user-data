#!/usr/bin/env python3
"""
A Log Filtering Module
"""

import re
import logging
import os as os
from typing import List
import mysql.connector

with open("user_data.csv") as f:
    piis = f.readline()[:-1]  # remove newline char
piis = piis.split(',')
#  print(piis)
piis.pop(5)
piis.pop(5)
piis.pop(5)
#  print(piis)
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
    print("Filter Datum: {}".format(message))
    for field in fields:
        p = (rf'({re.escape(field)}=)'
             rf'[^{re.escape(separator)})]+'
             rf'({re.escape(separator)})')
        message = re.sub(p, rf'\1{redaction}\2', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a new Logger instance """
    logger = logging.Logger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()  # handler
    handler.setFormatter(RedactingFormatter(PII_FIELDS))  # formatter

    logger.addHandler(handler)  # add handler to logger
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connects to a DB using ENV variables"""

    if os.getenv("PERSONAL_DATA_DB_USERNAME"):
        DB_USER = os.getenv("PERSONAL_DATA_DB_USERNAME")
    else:
        DB_USER = "root"

    if os.getenv("PERSONAL_DATA_DB_HOST"):
        DB_HOST = os.getenv("PERSONAL_DATA_DB_HOST")
    else:
        DB_HOST = "localhost"

    if os.getenv("PERSONAL_DATA_DB_HOST"):
        DB_PASS = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    else:
        DB_PASS = ""

    DB_NAME = os.getenv("PERSONAL_DATA_DB_NAME")

    # Create connection object
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    except Exception as exc:
        conn = ""
        raise exc

    return conn


def main():
    """Main function
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM users')

    logger = get_logger()
    for x in cursor:
        x = list(x)
        x[6] = str(x[6])

        start = x[:4]
        rem = x[4:]

        _str = ';'.join(start) + ";"
        _str = _str.replace(" ","")
        x = _str.split(";")
        x.pop()  # Issue: Stray whitespace after split is popped
        x = x + rem
        # Make a string val
        msg = "name={};email={};phone={};ssn={};password={};ip={};last_login={};user_agent={};".format(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]
        )
        logger.info(msg)


if __name__ == "__main__":
    main()
