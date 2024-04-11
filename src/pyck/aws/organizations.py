from pyck.aws.account import AwsAccount
from pyck.aws.service import Service


class Organizations(Service):
    def __init__(self, aws_account: AwsAccount):
        """Initiate an AWS Organizations helper"""
        self.client = aws_account.session.client("organizations")

    def get_accounts(self):
        """Get accounts in AWS Organizations"""
        result = super().get(self.client, "list_accounts", "Accounts")
        return [
            {"Id": o["Id"], "Name": o["Name"]}
            for o in result
            if o["Status"] == "ACTIVE"
        ]
