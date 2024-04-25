from pyck.aws.account import AwsAccount
from pyck.aws.organizations import Organization
from pyck.helpers.taskmanager import TaskManager


def organization_map(
    payer_account: AwsAccount,
    role_to_assume: str,
    func,
    parameters: list,
    aws_cli_profile: str = "default",
) -> tuple[list[any], list[Exception]]:
    "Loop through an AWS organization and invoke a function for each account in the organization. The invoked function needs to accept 2 parameters of type 'AwsAccount' and 'list' respectively"
    org = Organization(payer_account)
    accounts = org.get_accounts()
    results = []
    tm = TaskManager()

    for account in accounts:
        aws_account = AwsAccount.from_assuming_role(
            account["id"], role_to_assume, aws_cli_profile
        )
        if aws_account is not None:
            tm.add_task(func, parameters=[aws_account] + parameters)
    results, exceptions = tm.run_tasks()
    return results, exceptions
