import math
import re
import sys
import uuid
from datetime import datetime
from typing import Any, Sequence, Mapping

# define set of regex patterns for known field types

email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
request_id = r'^[0-9a-f]{32}$'
query_pattern = r'.+'


def validate(data: Any, **kwargs):
    """
    Validate the various parameters for url or form fields. The selected types of data
    are: bool, int, float, string, and uuid
    """

    def _check_bool_types(a: bool):
        return isinstance(a, bool)

    def _check_bool_list(a: Any):
        if isinstance(a, Sequence):
            return len([x for x in a if isinstance(x, bool)]) == len(a)

    def _check_datetime_types(a: datetime):
        return isinstance(a, datetime)

    def _check_dict_types(a: bool, keys: Sequence = None, values: Sequence = None):
        if not isinstance(a, Mapping):
            return False
        allowed_keys = None
        _dict = {}
        if keys:
            allowed_keys = [x for x in keys if isinstance(x, str) and len(x) < 256]
        if values:
            _dict = dict(zip(allowed_keys, values))
        if not (keys and values):
            return True
        else:
            return _dict

    def _check_float_types(arg: float, value: float = None, start: float = None,
                           end: float = None,
                           approved: Sequence = None):
        if not isinstance(arg, float):
            return False
        float_max = float('inf')
        float_min = float('-inf')

        try:
            _arg = arg if (arg < float_max) and (arg > float_min) else None
            if value:
                return math.isclose(_arg, value)
            if end:
                return _arg <= end
            if start:
                return _arg >= start

            approved_values = [x for x in approved if isinstance(x, float)] \
                if isinstance(approved, Sequence) else []
            if approved_values:
                return _arg in approved_values
            return bool(_arg)
        except ValueError:
            return False
        except Exception:
            return False

    def _check_int_types(arg: int, value: int = None, start: int = None, end: int = None,
                         approved: Sequence = None):
        if not isinstance(arg, int):
            return False
        int_min = -sys.maxsize - 1
        int_max = sys.maxsize
        try:
            _arg = int(arg) if (arg < int_max) and (arg > int_min) else None

            if value:
                return _arg == value
            if end:
                return _arg <= end
            if start:
                return _arg >= start

            approved_values = [x for x in approved if isinstance(x, int)] \
                if isinstance(approved, Sequence) else []
            if approved_values:
                return _arg in approved_values
            return bool(_arg)
        except ValueError:
            return False
        except Exception:
            return False

    def _check_str(a: str, patterns: Any = None, length: int = None,
                   approved: Sequence = None):
        if not isinstance(a, (str, bool, int, float)):
            a = str(a)

        if not (patterns or length or approved):
            return len(a) < 256

        if isinstance(patterns, (tuple, list)) and length:
            approved_patterns = map(lambda x: re.compile(x), patterns)
            return all([
                    x for x in approved_patterns if
                    x.match(a) and (len(a) < 256 or len(a) <= length)
            ])
        if isinstance(patterns, str):
            if re.compile(patterns).match(a):
                return True
        if isinstance(approved, Sequence):
            return a in approved
        return bool(a)

    def _check_uuid_types(a: uuid.UUID):
        if isinstance(a, uuid.UUID):
            return True
        elif isinstance(a, (str, int, bytes, tuple)):
            try:
                if isinstance(a, str):
                    return uuid.UUID(hex=a) and True
                elif isinstance(a, int):
                    return uuid.UUID(int=a) and True
                elif isinstance(a, bytes):
                    return (uuid.UUID(bytes=a) or uuid.UUID(bytes_le=a)) and True
                elif isinstance(a, tuple):
                    return uuid.UUID(fields=a)
            except ValueError:
                return False

    return _check_uuid_types(data) or _check_bool_types(data) \
           or _check_bool_list(data) or _check_datetime_types(data) \
           or _check_dict_types(data, keys=kwargs.get('keys'), values=kwargs.get(
            'values')) \
           or _check_int_types(data, start=kwargs.get('start'), end=kwargs.get('end'),
                               approved=kwargs.get('approved')) \
           or _check_float_types(data, start=kwargs.get('start'), end=kwargs.get('end'),
                                 value=kwargs.get('value'), approved=kwargs.get(
                'approved')) \
           or _check_str(data, patterns=kwargs.get('patterns'), length=kwargs.get(
            'length'), approved=kwargs.get('approved'))
