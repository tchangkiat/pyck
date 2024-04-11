from pyck.aws.account import AwsAccount


class EC2:
    def __init__(self, aws_account: AwsAccount):
        """Initiate an Amazon EC2 helper"""
        self.client = aws_account.session.client("ec2")

    def get_valid_regions(self, filter: list[str] = []):
        """Get valid regions of the AWS account"""
        if len(filter) == 0:
            return [
                r["RegionName"]
                for r in self.client.describe_regions(AllRegions=False)["Regions"]
            ]
        else:
            return [
                r["RegionName"]
                for r in self.client.describe_regions(AllRegions=False)["Regions"]
                if r["RegionName"] in filter
            ]
