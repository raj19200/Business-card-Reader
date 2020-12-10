import re

def is_pincode(txt):
    p = re.findall(r'([1-9]{1}[0-9]{5}|[1-9]{1}[0-9]{2}[ -][0-9]{3})(?!\d)',txt)
    return p