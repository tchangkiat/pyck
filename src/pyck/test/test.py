from pyck.helpers.logging import Logging
from pyck.helpers.taskmanager import TaskManager
from pyck.utils.styles import purple
from pyck.aws.account import AwsAccount
from pyck.aws.ec2 import EC2


def test_task(random_text):
    print("test_task " + random_text)
    return "return value"


def test_task_exception():
    print("test_task_exception")
    ex = Exception("Test raising an Exception in a task")
    ex.resources = ["Google: https://google.com"]
    raise ex


log = Logging.get_instance()
log.info(purple("\nTesting Task Manager"))
tm = TaskManager()
tm.add_task(test_task, parameters=["hello 1", "hello 2", "hello 3"])
tm.run_tasks("Task Manager - Don't Wait", wait=False)
tm2 = TaskManager()
tm2.add_task(test_task_exception)
tm2.add_task(test_task, parameters=["hello 4"])
results, exceptions = tm2.run_tasks("Task Manager 2 - Exception")

log.info(purple("\nTesting AWS-related helpers and utilities"))
aws_account = AwsAccount.from_profile()
print("AWS Account ID: " + str(aws_account))
aws_account = AwsAccount.from_assuming_role("409989946510", "container-baseline-review")
print("Assumed Role of AWS Account ID: " + str(aws_account))
ec2_helper = EC2(aws_account)
valid_regions = ec2_helper.get_valid_regions()
print("Valid Regions: " + ", ".join(valid_regions))
