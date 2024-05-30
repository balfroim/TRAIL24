
from functools import wraps
import os
import pickle


def cache_to_file(file_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    result = pickle.load(file)
            else:
                result = func(*args, **kwargs)
                with open(file_path, 'wb') as file:
                    pickle.dump(result, file)
            return result
        return wrapper
    return decorator