from pyck.aws.account import AwsAccount
from pyck.aws.organizations import Organization
from pyck.helpers.taskmanager import TaskManager


def organization_map(
    aws_account: AwsAccount, role_to_assume: str, func, parameters: list
) -> tuple[list[any], list[Exception]]:
    "Loop through an AWS organization and invoke a function for each account in the organization. The function needs to accept 2 parameters of type 'AwsAccount' and 'list' respectively"
    org = Organization(aws_account)
    accounts = org.get_accounts()
    results = []
    tm = TaskManager()

    for account in accounts:
        aws_account = AwsAccount.from_assuming_role(account["id"], role_to_assume)
        if aws_account is not None:
            tm.add_task(func, parameters=[aws_account] + parameters)
    results, exceptions = tm.run_tasks()
    return results, exceptions
