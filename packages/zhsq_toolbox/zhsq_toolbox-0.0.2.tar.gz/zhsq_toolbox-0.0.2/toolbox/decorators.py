import functools
import traceback
from multiprocessing.pool import ThreadPool


def timeout(max_timeout=2):
    """Timeout decorator, parameter in seconds."""

    def deco(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            return async_result.get(max_timeout)

        return func_wrapper

    if callable(max_timeout):
        # Check if timeout was used without parentheses
        func, max_timeout = max_timeout, 2
        return deco(func)
    return deco


def response_error(verbose=False):
    """
    A useful debug decorator to display error at page, when debug=False.
    Do do not use it at product environment unless you are debugging at server.
    """

    def deco(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                from django.http import HttpResponse

                if verbose:
                    debug_info = traceback.format_exc().replace("\n", "<br>")
                    return HttpResponse(debug_info)
                return HttpResponse(f'<h1 style="color:red">{e}!</h1>')

        return wrap

    if callable(verbose):
        # Check if response_error was used without parentheses
        func, verbose = verbose, False
        return deco(func)

    return deco
