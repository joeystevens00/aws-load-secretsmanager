import boto3
import requests
import re
import json
import sys
import os

def get_region():
    if os.environ.get('AWS_REGION'):
        return os.environ['AWS_REGION']
    try:
        response = requests.get('http://169.254.169.254/latest/meta-data/placement/region')
        return response.text
    except requests.exceptions.ConnectionError as e:
        exit("Unable to reach EC2 metadata service. If not running from within EC2 then set the AWS_REGION environment variable.")

def get_instance_id():
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    return response.text

def ec2():
    return boto3.client('ec2', get_region())

def format_variables(s):
    return [x.strip('{').strip('}') for x in re.findall("{[a-zA-Z0-9]+}", s)]

def load_variables(s):
    if format_variables(s):
        instance_metadata=ec2().describe_instances(InstanceIds=[get_instance_id()])
        tags = instance_metadata['Reservations'][0]['Instances'][0]['Tags']
        return s.format(**{tag['Key']: tag['Value'] for tag in tags})
    else:
        return s

def get_secrets(secret_id):
    secretsmanager = boto3.client('secretsmanager', get_region())
    secret = secretsmanager.get_secret_value(SecretId=secret_id)
    return json.loads(secret['SecretString'])

if __name__ == "__main__":
    secret_id = load_variables(sys.argv[1])
    secrets = get_secrets(secret_id)
    for k, v in secrets.items():
        v = v.replace('"', '\\"')
        print(f"export {k}=\"{v}\"")
