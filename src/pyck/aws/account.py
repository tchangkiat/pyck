import boto3


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
        if profile:
            session = boto3.Session(profile_name=profile)
        else:
            session = boto3.Session()
        credentials = session.get_credentials().get_frozen_credentials()
        return cls(credentials.access_key, credentials.secret_key, credentials.token)

    @classmethod
    def from_assuming_role(
        cls,
        account_id: str,
        role_name: str,
        profile_to_assume_role: str = "default",
    ):
        """Create an AwsAccount object based on assumed role"""
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
