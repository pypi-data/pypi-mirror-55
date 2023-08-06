# -*- encoding: utf-8 -*-
import os


def get_env_variable(key):
    """
    Get the environment variable or return exception
    Copied from Django two scoops book
    """
    try:
        return os.environ[key]
    except KeyError:
        error_msg = "Set the {} env variable".format(key)
        print("ImproperlyConfigured: {}".format(error_msg))
        raise ImproperlyConfigured(error_msg)


def get_env_variable_bool(key):
    """
    Retrieves env vars and makes Python boolean replacements
    Copied from
    http://www.wellfireinteractive.com/blog/easier-12-factor-django/
    """
    result = get_env_variable(key)
    if result == "True":
        result = True
    elif result == "False":
        result = False
    else:
        error_msg = """
        The {} variable must be set to 'True' or 'False': {}""".format(
            key, result
        )
        print("ImproperlyConfigured: {}".format(error_msg))
        raise ImproperlyConfigured(error_msg)
    return result
