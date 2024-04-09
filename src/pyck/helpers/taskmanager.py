from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import traceback

from pyck.helpers import logging


class ThreadPoolExecutorStackTraced(ThreadPoolExecutor):
    def submit(self, fn, *args, **kwargs):
        """Submits the wrapped function instead of `fn`"""
        return super(ThreadPoolExecutorStackTraced, self).submit(
            self._function_wrapper, fn, *args, **kwargs
        )

    def _function_wrapper(self, fn, *args, **kwargs):
        """Wraps `fn` in order to preserve the traceback of any kind of
        raised exception"""
        log = logging.Logging.get_instance()
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            log.error(sys.exc_info()[0](traceback.format_exc()))


class TaskManager:
    def __init__(self):
        """Initiate a Task Manager."""
        self.tasks = []

    def add_task(self, function, parameters: list = ""):
        """Add task to run later."""
        self.tasks.append({"function": function, "parameters": parameters})

    def run_tasks(self, description: str = "", wait: bool = True):
        """Run tasks that are added"""
        results = []
        executor = ThreadPoolExecutorStackTraced(max_workers=10)
        futures = []
        if description:
            print(description)
        for task in self.tasks:
            if task["parameters"] and type(task["parameters"]) is not list:
                futures = [executor.submit(task["function"], task["parameters"])]
            elif type(task["parameters"]) is list:
                futures = [
                    executor.submit(task["function"], parameter)
                    for parameter in task["parameters"]
                ]
            else:
                futures = [executor.submit(task["function"])]
        if wait:
            with alive_bar(len(futures)) as bar:
                for future in as_completed(futures, timeout=10):
                    exception = future.exception()
                    if not exception:
                        results.append(future.result())
                    else:
                        results.append(exception)
                    bar()
            executor.shutdown()
        else:
            executor.shutdown(wait=False)
        self.tasks = []  # Clear tasks
        return results
