# -*- coding: utf-8 -*-

from functools import wraps
from inspect import isfunction

model_list = []
function_list = []


def collect(description):
    def decorator(m):
        f_list = list(filter(lambda f: not f.startswith('__'), dir(m)))
        model = '.'.join([m.__module__, m.__name__])
        function_dict = {}
        for f in f_list:
            func = getattr(m, f)
            if isfunction(func):
                func_name = func.__name__
                func_description = func.__doc__
                func_id = '.'.join([model, func_name])
                function_dict.update({
                    "name": func_name,
                    "description": func_description.split(':')[0].strip('\n '),
                    "_id": func_id,
                    "active": True,
                    "model": model
                })
        model_list.append({'name': model, 'description': description, '_id': model})
        if function_dict:
            function_list.append(function_dict)

        @wraps(m)
        def decorator_function(*args, **kwargs):
            return m(*args, **kwargs)
        return decorator_function
    return decorator
