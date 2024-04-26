from pyck.aws.account import AwsAccount
from pyck.aws.organizations import Organization


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

    for account in accounts:
        aws_account = AwsAccount.from_assuming_role(
            account["id"], role_to_assume, aws_cli_profile
        )
        results.append(func(aws_account, *parameters))
    return results
