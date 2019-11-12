import io
from contextlib import redirect_stdout
import re
from PyInquirer import prompt
import sys
import datetime

def to_dict(obj, verbose=False):
    VERBOSE_FIELDS = ['content_related', 'out', 'mentioned', 'media_unread',
        'silent', 'confirm_received', 'content_related']

    if isinstance(obj, list):
        return [to_dict(values) for values in obj]
    class_name = type(obj).__name__
    obj = obj.__dict__
    obj['class'] = class_name

    if not verbose:
        obj = {k: v for k, v in obj.items() if k not in VERBOSE_FIELDS and v is not None}

    for key, values in obj.copy().items():
        if re.match('_.*', key):
            del obj[key]
            continue
        if hasattr(values, '__dict__'):
            obj[key] = to_dict(values)
            continue
        if isinstance(values, datetime.date):
            obj[key] = obj[key].isoformat()
            continue
        if isinstance(values, bytes):
            del obj[key]
            continue
        if isinstance(values, list):
            for i in range(len(values)):
                if (hasattr(values[i], '__dict__')):
                    obj[key][i] = to_dict(values[i])
    return obj

def prompt_info(info):
    # Following block allows you to exit properly with ctrl+c
    f = io.StringIO()
    with redirect_stdout(f):
        user = prompt(info)
    out = f.getvalue()
    if (re.search("Cancelled by user", out)):
        sys.exit(1)
    return user
