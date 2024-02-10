#!/usr/bin/env python3
import re
"""
filtered logger
"""

def filter_datum(fields, redaction, message, separator):
    """
    Regex-ing
    """
    new_message = message
    for field in fields:
        new_message = re.sub(f"(?<={field}=)[^{separator}]*",
                              redaction,
                              new_message,
                              count=0,
                              flags=0)
    return new_message
