#!/usr/bin/env python3
import re
from typing import List
"""
filtered logger
"""

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Regex-ing
    """
    new_message = message
    for field in fields:
        new_message = re.sub(f"(?<={field}=)[^{separator}]*", redaction, new_message, count=0, flags=0)
    return new_message
