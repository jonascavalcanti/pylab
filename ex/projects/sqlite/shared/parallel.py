from concurrent import futures
from typing import List

from loguru import logger

from shared import Env


class ParallelExecResult:
    """Holds information about a list of parallel background tasks execution
    """
    def __init__(self):
        self.errors = []
        self.results = []

    def has_errors(self):
        """Checks a list of parallel background tasks execution and returns TRUE
        if any of them have errors
        """
        return len(self.errors) > 0


def execute(method: callable, args_list: List[dict]) -> ParallelExecResult:
    """Runs background tasks in parallel, wait for them all to
    complete and returns result data all at once.

    :param method
        Callable method or function to be executed in background
    :param args_list
        List of parameters to be passed to the method as **kwargs
    """
    result = ParallelExecResult()
    threads = []
    max_workers = None
    if int(Env.MAX_WORKERS) > 0:
        max_workers = int(Env.MAX_WORKERS)
    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for kwargs in args_list:
            threads.append(
                executor.submit(method, **kwargs))

    results = futures.wait(threads)

    result.errors = [
        result.exception() for result in results.done if result.exception() is not None]
    for error in result.errors:
        logger.error(error)

    if len(result.errors) == 0:
        result.results = [result.result() for result in results.done]

    return result
