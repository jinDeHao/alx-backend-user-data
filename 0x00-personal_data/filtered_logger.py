#!/usr/bin/env python3
"""
filtered logger
"""
import csv
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

    def __init__(self, fields: List[str]):
        """
        class constructor
        """
        self.__fields = fields
        super().__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records
        using filter_datum
        """
        record.msg = filter_datum(self.__fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Create logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter)
    logger.addHandler(handler)
    return logger


PII_FIELDS: List[str]


"""Open the CSV file"""
with open('user_data.csv', 'r') as file:
    """
    Create a CSV reader object
    """
    csv_reader = csv.reader(file)

    PII_FIELDS = [f for f in list(csv_reader)[0] if f != 'Count']
