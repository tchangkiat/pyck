import boto3
from botocore.exceptions import ProfileNotFound, ClientError

from pyck.helpers.logging import Logging


class AwsAccount:
    def __init__(self, access_key: str, secret_key: str, token: str):
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=token,
        )
        self.account_id = (
            self.session.client("sts").get_caller_identity().get("Account")
        )

    def __str__(self):
        return self.account_id

    @classmethod
    def from_profile(cls, profile: str = "default"):
        """Create an AwsAccount object using credentials of AWS CLI profile"""
        try:
            if profile:
                session = boto3.Session(profile_name=profile)
            else:
                session = boto3.Session()
            credentials = session.get_credentials().get_frozen_credentials()
            return cls(
                credentials.access_key, credentials.secret_key, credentials.token
            )
        except ProfileNotFound as e:
            log = Logging.get_instance()
            log.error(
                "Unable to find the AWS CLI profile '"
                + e.__dict__["kwargs"]["profile"]
                + "'. ",
                resources=[
                    "Configure a profile for AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html"
                ],
            )

    @classmethod
    def from_assuming_role(
        cls,
        account_id: str,
        role_name: str,
        profile_to_assume_role: str = "default",
    ):
        """Create an AwsAccount object based on assumed role"""
        try:
            aws_account = cls.from_profile(profile_to_assume_role)
            client = aws_account.session.client("sts")
            response = client.assume_role(
                RoleArn="arn:aws:iam::" + account_id + ":role/" + role_name,
                RoleSessionName=account_id + "-" + role_name,
            )
            credentials = response["Credentials"]
            return cls(
                credentials["AccessKeyId"],
                credentials["SecretAccessKey"],
                credentials["SessionToken"],
            )
        except ClientError as e:
            log = Logging.get_instance()
            if "(AccessDenied) when calling the AssumeRole operation" in str(e):
                log.error(
                    "Unable to assume role '"
                    + "arn:aws:iam::"
                    + account_id
                    + ":role/"
                    + role_name
                    + "'. Ensure that the profile has permission to perform 'sts:AssumeRole', the role exists, and the management account is added as a trust entity in the role.",
                    resources=[
                        "Use trust policies with IAM roles: https://aws.amazon.com/blogs/security/how-to-use-trust-policies-with-iam-roles/"
                    ],
                )
