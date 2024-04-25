from pyck.aws.account import AwsAccount
from pyck.aws.service import Service
from pyck.helpers.logging import Logging


class Organization(Service):
    def __init__(self, aws_account: AwsAccount):
        """Initiate an AWS Organizations object with a payer account"""
        self.client = aws_account.session.client("organizations")

    def get_accounts(self):
        """Get accounts in the AWS organization"""
        try:
            result = super().get(self.client, "list_accounts", "Accounts")
            return [
                {"id": o["Id"], "name": o["Name"]}
                for o in result
                if o["Status"] == "ACTIVE"
            ]
        except Exception as e:
            log = Logging.get_instance()
            if (
                "(AccessDeniedException) when calling the ListAccounts operation"
                in str(e)
            ):
                log.error(
                    "Unable to retrieve the list of accounts in the organization. Please check if the profile has the 'organizations:ListAccounts' permission"
                )
