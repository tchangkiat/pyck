import time

from pyck.helpers.logging import Logging
from pyck.helpers.taskmanager import TaskManager


def test_task(sleep_duration=1.0):
    time.sleep(sleep_duration)


log = Logging.get_instance()
log.info("This is an info message")
log.debug("This is a debug message")
log.error("This is an error message", "Additional message")

tm = TaskManager()
tm.add_task(test_task, parameters=[1.0, 2.0, 3.0])
tm.run_tasks("Test Task Manager")
