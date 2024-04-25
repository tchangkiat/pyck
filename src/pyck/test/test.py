from pyck.helpers.logging import Logging
from pyck.helpers.taskmanager import TaskManager
from pyck.utils.styles import purple
from pyck.aws.account import AwsAccount
from pyck.aws.ec2 import EC2
from pyck.aws.organizations import Organization
from pyck.aws.utils import organization_map


def test_task(random_text):
    print("test_task " + random_text)
    return "return value"


def test_task_exception():
    print("test_task_exception")
    ex = Exception("Test raising an Exception in a task")
    ex.resources = ["Google: https://google.com"]
    raise ex


def print_assumed_account_id(aws_account: AwsAccount, assumed_role: str):
    if aws_account is not None:
        print(
            "Assumed Role '"
            + str(assumed_role)
            + "' of AWS Account ID: "
            + str(aws_account)
        )


log = Logging.get_instance()
log.info(purple("\nTesting Task Manager"))
tm = TaskManager()
tm.add_multiple_tasks_by_parameters(
    test_task, parameters=[["hello 1"], ["hello 2"], ["hello 3"]]
)
tm.run_tasks("Task Manager - Don't Wait", wait=False)
tm2 = TaskManager()
tm2.add_task(test_task_exception)
tm2.add_task(test_task, parameters=["hello 4"])
results, exceptions = tm2.run_tasks("Task Manager 2 - Exception")

log.info(purple("\nTesting AWS-related helpers and utilities"))
aws_account = AwsAccount.from_profile()
print("AWS Account ID: " + str(aws_account))
print("Accounts in AWS Organizations:")
org_helper = Organization(aws_account)
accounts = org_helper.get_accounts()
print(accounts)
organization_map(
    aws_account,
    "container-baseline-review",
    print_assumed_account_id,
    ["container-baseline-review"],
)
