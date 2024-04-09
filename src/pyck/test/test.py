import time
import traceback

from pyck.helpers.logging import Logging
from pyck.helpers.taskmanager import TaskManager
from pyck.utils.styles import purple


def test_task(random_text):
    print("test_task " + random_text)
    return "return value"


def test_task_exception():
    print("test_task_exception")
    raise Exception("Test Exception")


log = Logging.get_instance()
log.info("This is an info message")
log.debug("This is a debug message")
tm = TaskManager()
tm.add_task(test_task, parameters=["hello 1", "hello 2", "hello 3"])
tm.run_tasks("Test Task Manager - Don't Wait", wait=False)
tm2 = TaskManager()
tm2.add_task(test_task_exception)
tm2.add_task(test_task, parameters=["hello 4"])
results, exceptions = tm2.run_tasks("Test Task Manager 2 - Exception")
print(results)
print(exceptions)
log.error(
    "".join(
        traceback.format_exception(
            type(exceptions[0]), value=exceptions[0], tb=exceptions[0].__traceback__
        )
    ),
    "This exception is intentional - it tests the exception catching in concurrent.futures and logging of an error message.",
)
