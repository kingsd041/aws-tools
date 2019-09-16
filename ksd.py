import logging
import boto3
import time
import paramiko
from botocore.exceptions import ClientError
from utils.connect_to_instance import *

# Provision and launch the EC2 instance
ec2_client = boto3.client('ec2', 'ca-central-1')

def create_ec2_instance(instance_type,
                        keypair_name,
                        security_group,
                        block_device_mapping,
                        image_id,
                        min_count,
                        max_count,
                        tag_specifications,):
    """Provision and launch an EC2 instance

    The method returns without waiting for the instance to reach
    a running state.

    :param image_id: ID of AMI to launch, such as 'ami-XXXX'
    :param instance_type: string, such as 't2.micro'
    :param keypair_name: string, name of the key pair
    :return Dictionary containing information about the instance. If error,
    returns None.
    """

    # Provision and launch the EC2 instance
    # ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            MinCount=min_count,
                                            MaxCount=max_count,
                                            SecurityGroupIds=security_group,
                                            BlockDeviceMappings=block_device_mapping,
                                            TagSpecifications=tag_specifications
                                            )
    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]


def create_instance_tags(instance_id, tag_name, tag_value):
    # Provision and launch the EC2 instance
    # ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.create_tags(
            Resources=[
                instance_id,
            ],
            Tags=[
                {'Key': tag_name,
                 'Value': tag_value},
            ],
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response


def get_instance_public_ip(instance_id):
    for _ in range(10):
        time.sleep(2)
        response = ec2_client.describe_instances(
            InstanceIds=[
                instance_id,
            ],
        )
        instance_public_ip = response["Reservations"][0]["Instances"][0]["PublicIpAddress"]
        if instance_public_ip is not None:
            break
    return instance_public_ip


def install_docker(instance_ip, ssh_username='ubuntu'):
    logging.info(f'Installing docker...')
    install_docker_command = 'curl https://releases.rancher.com/install-docker/18.09.sh | sh -'
    ssh_client = connection(instance_ip, ssh_username, seconds=2)
    result = executor(ssh_client, install_docker_command)
    return result
