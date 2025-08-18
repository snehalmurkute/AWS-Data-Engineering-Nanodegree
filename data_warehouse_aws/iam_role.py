def create_dwh_iam():
    import json
    import boto3
    print('1.1 Creating a new IAM Role')
    iam_client = boto3.client('iam', region_name="us-west-2")
    dwhRole = iam_client.create_role(Path='/', RoleName="dwh_user",
                                     Description="Allows Redshift clusters to call AWS services on your behalf.",
                                     AssumeRolePolicyDocument=json.dumps(
                                         {'Statement': [{'Action': 'sts:AssumeRole',
                                                         'Effect': 'Allow',
                                                         'Principal': {'Service': 'redshift.amazonaws.com'}}],
                                          'Version': '2012-10-17'}))


if __name__ == '__main__':
    create_dwh_iam()
