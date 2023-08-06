from functools import wraps
from flask import request, jsonify

"""
This file contains various helper functions implemented as decorators.
"""


def __missing_fields(body, required_fields: list = None) -> list:
    """
    missing_fields returns a list of keys missing from the `body` dict.
    :param dict body: parsed object
    :param required_fields: list of non-optional keys in body
    :return list:
    """
    if required_fields is not None:
        # gather all (if any) missing fields
        return [f for f in required_fields if f not in body]
    return []


def parse_json(var_name: str, required_fields: list = None):
    """
    parse_json parses the request body as JSON, and injects it into the function's keyword arguments named `var_name`.

    Example:
        @parse_json(body, required_fields=['id', 'name'])
        def some_function(body):
          print(body['id'])

    :param str var_name: variable name to populate with request body
    :param list required_fields: optional list of fields to ensure are present in request body
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_json(force=True)
            # return error with list of missing fields
            missing = __missing_fields(body, required_fields)
            if len(missing) > 0:
                return jsonify(error=f"missing required fields: {','.join(missing)}"), 400
            kwargs[var_name] = body
            return func(*args, **kwargs)
        return wrapper
    return decorator


def parse_query(var_name: str, required_fields: list = None):
    """
    parse_query parses the query parameters as a dict, and injects them into the function's keyword arguments named 'var_name'.

    Example:
        @parse_query(params, required_fields=['id'])
        def some_function(params):
            print(params['id'])

    :param str var_name: variable name to populate request body
    :param list required_fields: optional list of fields to ensure are present in query parameters
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            params = request.args.to_dict()
            missing = __missing_fields(params, required_fields)
            if len(missing) > 0:
                return jsonify(error=f"missing required fields: {','.join(missing)}"), 400
            kwargs[var_name] = params
            return func(*args, **kwargs)
        return wrapper
    return decorator
