#!/usr/bin/env python3
"""
filtered logger
"""
import re
from typing import List
import logging


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Regex-ing
    """
    new_message = message
    for field in fields:
        new_message = re.sub(f"(?<={field}=)[^{separator}]*",
                             redaction,
                             new_message,
                             count=0, flags=0)
    return new_message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        class constructor
        """
        self.__fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records
        using filter_datum
        """
        return filter_datum(self.__fields,
                            self.REDACTION,
                            record,
                            self.SEPARATOR)
