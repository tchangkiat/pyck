from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed


class TaskManager:
    def __init__(self):
        """Initiate a Task Manager."""
        self.tasks = []

    def add_task(self, function, parameters: list = None):
        """Add task to run later."""
        self.tasks.append({"function": function, "parameters": parameters})

    def run_tasks(self, description: str = "", wait: bool = True):
        """Run tasks that are added"""
        results = []
        exceptions = []
        executor = ThreadPoolExecutor(max_workers=10)
        futures = []
        if description:
            print(description)
        for task in self.tasks:
            if type(task["parameters"]) is list:
                futures = futures + [
                    executor.submit(task["function"], parameter)
                    for parameter in task["parameters"]
                ]
            else:
                if task["parameters"] is not None:
                    futures = futures + [
                        executor.submit(task["function"], task["parameters"])
                    ]
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
        return results, exceptions
