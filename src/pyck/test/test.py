import time

from pyck.helpers.logging import Logging
from pyck.helpers.taskmanager import TaskManager
from pyck.utils.styles import purple


def test_task(random_text):
    print("test_task " + random_text)
    return "return value"


def test_task_exception():
    raise Exception("Test Exception")


log = Logging.get_instance()
log.info("This is an info message")
log.debug("This is a debug message")
log.error("This is an error message", "Additional message")
log.info(purple("This is a purple text"))

tm = TaskManager()
tm.add_task(test_task, parameters=["hello 1", "hello 2", "hello 3"])
tm.run_tasks("Test Task Manager - Don't Wait", wait=False)
tm2 = TaskManager()
tm2.add_task(test_task_exception)
tm2.add_task(test_task, parameters=["hello 4"])
results = tm2.run_tasks("Test Task Manager - Exception")
print(results)
