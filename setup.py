import boto3

# Replace these with your own values
region = 'us-west-2'
ami_id = 'ami-0c55b159cbfafe1f0'
instance_type = 't2.micro'
key_name = 'my-key-pair'
security_group_name = 'flask-app-sg'
flask_app_path = '/path/to/your/flask/app'
flask_app_port = 5000
ssh_port = 22
pem_file_path = '/path/to/your/pem/file'

# Create a new EC2 client
ec2 = boto3.client('ec2', region_name=region)

# Create a new security group for the Flask app
response = ec2.create_security_group(
    Description='Flask App Security Group',
    GroupName=security_group_name,
)
security_group_id = response['GroupId']

# Allow TCP traffic on the Flask app port
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': flask_app_port,
            'ToPort': flask_app_port,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
    ]
)

# Allow SSH traffic on port 22
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': ssh_port,
            'ToPort': ssh_port,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
    ]
)

# Launch a new EC2 instance
response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=[security_group_id],
    MinCount=1,
    MaxCount=1,
    UserData=f'''#!/bin/bash
sudo yum -y update
sudo yum -y install python3 git
git clone https://github.com/yourusername/yourflaskapp.git
cd {flask_app_path}
sudo pip3 install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port={flask_app_port} &
''',
)
instance_id = response['Instances'][0]['InstanceId']

print(f'Launching instance {instance_id}...')
