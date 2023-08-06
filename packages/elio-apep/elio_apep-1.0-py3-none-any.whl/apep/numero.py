# -*- coding: utf-8 -*

def roundy(x, prec=1, base=0.5):
    """Round a number to fixed decimal places."""
    if not x:
        x = 0
    return round(base * round(float(x) / base), prec)


def is_number(s):
    """Determine whether a string can be safely converted to a number."""
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
