""" Define a wrapper class to collect exceptions that are
raised at runtime. Users can pass an instance of the object
that can get affected because of the exception"""

from typing import Callable
from functools import wraps

def format_error_string(error: str, affected_object: str) -> str:
    """
    Joins and formats two given strings,
    returns a single string
    """
    return '<br>'.join(
        [
            "ERROR: ",
            error,
            "AFFECTED OBJECT:",
            affected_object,
            "================================================================",
            "",
        ]
    )

class CollectErrors():
    """ A wrapper class to collect exceptions in a file at runtime """
    def __init__(
            self,
        exceptions: tuple,
            runtime_object = None,
    ) -> None:
        self.runtime_object = runtime_object
        self.exceptions = exceptions

    def __call__(self, func: Callable) -> Callable:
        """ Decorate the function and return it """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """ The wrapper for the function """
            print("Inside the wrapper")
            outfile = "errors.txt"
            try:
                return func(*args, **kwargs)
            except self.exceptions as error:
                with open(outfile, "a+") as out_file:
                    out_file.write(
                        format_error_string(
                            str(error),
                            str(self.runtime_object),
                        )
                    )

        return wrapper

