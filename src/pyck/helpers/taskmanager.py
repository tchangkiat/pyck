from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed

from pyck.helpers.logging import Logging


class TaskManager:
    def __init__(self):
        """Initiate a Task Manager."""
        self.tasks = []

    def add_task(self, function, parameters: list = None):
        """Add task to run later."""
        self.tasks.append({"function": function, "parameters": parameters})

    def add_multiple_tasks_by_parameters(self, function, parameters: list[list]):
        """Add multiple tasks (one task per parameter) to run later."""
        for parameter in parameters:
            self.tasks.append({"function": function, "parameters": parameter})

    def run_tasks(
        self, description: str = "", wait: bool = True, logExceptions=True
    ) -> tuple[list[any], list[Exception]]:
        """Run tasks that are added"""
        results = []
        exceptions = []
        executor = ThreadPoolExecutor(max_workers=10)
        futures = []
        if description:
            print(description)
        for task in self.tasks:
            if task["parameters"] is not None:
                futures.append(executor.submit(task["function"], *task["parameters"]))
            else:
                futures = futures + [executor.submit(task["function"])]
        if wait:
            with alive_bar(len(futures)) as bar:
                for future in as_completed(futures, timeout=10):
                    try:
                        results.append(future.result())
                    except:
                        exceptions.append(future.exception())
                    bar()
            executor.shutdown()
        else:
            executor.shutdown(wait=False)
        self.tasks = []  # Clear tasks
        if logExceptions:
            log = Logging.get_instance()
            for exception in exceptions:
                log.exception(
                    exception,
                    exception.resources if hasattr(exception, "resources") else [],
                )
        return results, exceptions
