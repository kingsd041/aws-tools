from re import I
import boto3
from botocore.exceptions import ClientError
from utils.connect_to_instance import *
import configparser
import os
import sys

root_dir = os.path.dirname(__file__)
aws_config_file = '/aws-config.conf'

config = configparser.ConfigParser()
config.read(root_dir + aws_config_file)
ec2_client = boto3.client('ec2', config.get('aws-config', 'region'))
ec2_resource = boto3.resource('ec2', config.get('aws-config', 'region'))


def create_ec2_instance(instance_type,
                        keypair_name,
                        security_group,
                        block_device_mapping,
                        image_id,
                        min_count,
                        max_count,
                        tag_specifications, ):
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
    install_docker_command = 'curl https://get.docker.com | VERSION=18.09 sh -s -'
    ssh_client = connection(instance_ip, ssh_username, seconds=2)
    result = executor(ssh_client, install_docker_command)
    return result


def list_instances():
    tplt = "{0:20}\t{1:20}\t{2:15}\t{3:15}\t{4:15}\t{5:15}\t{6:10}"
    print(
        tplt.format('InstanceId', 'InstanceName', 'PublicIp', 'PrivateIp', 'InstanceType', 'Instance_state', 'KeyName'))
    for instance in ec2_resource.instances.all():
        if instance.public_ip_address == None or instance.private_ip_address == None:
            public_ip = ''
            private_ip = ''
        else:
            public_ip = instance.public_ip_address
            private_ip = instance.private_ip_address
        for i in instance.tags:
            if i.get("Key") == "Name":
                instance_name = i.get("Value")

        print(tplt.format(instance.id, instance_name, public_ip, private_ip, instance.instance_type,
                          instance.state['Name'], instance.key_name))


def terminate_instances(instance_ids):
    # ec2 = boto3.client('ec2', 'ca-central-1')

    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    try:
        states = ec2_client.terminate_instances(InstanceIds=instance_ids)
    except ClientError as e:
        logging.error(e)
        return None

    return states['TerminatingInstances']


def terminate_instances_custom(instances_list_id, instances_list_name):
    if instances_list_id == []:
        print('There are no instances to delete！')
        return True

    confirm_operation = input('The following instance will be terminated?\n{}\n[y/n] '.format(instances_list_name))
    if confirm_operation == 'y':
        states = terminate_instances(instances_list_id)
    else:
        states = None

    if states is not None:
        logging.info('Terminating the following EC2 instances')
        for state in states:
            logging.info(f'ID: {state["InstanceId"]}')
            logging.info(f'  Current state: Code {state["CurrentState"]["Code"]}, '
                         f'{state["CurrentState"]["Name"]}')
            logging.info(f'  Previous state: Code {state["PreviousState"]["Code"]}, '
                         f'{state["PreviousState"]["Name"]}')
    return states


def terminate_all_instances():
    response = ec2_client.describe_instances()
    instances_list_id = []
    instances_list_name = []
    for ins_num in range(len(response['Reservations'])):
        instance_state = response['Reservations'][ins_num]['Instances'][0]['State']['Name']
        if instance_state != 'terminated':
            instance_id = response['Reservations'][ins_num]['Instances'][0]['InstanceId']
            instance_name = response['Reservations'][ins_num]['Instances'][0]['Tags'][0]['Value']
            instances_list_id.append(instance_id)
            instances_list_name.append(instance_name)
    terminate_instances_custom(instances_list_id, instances_list_name)


def instance_id_conversion_name(instance_id):
    instance_name = []
    for ins_id in instance_id:
        try:
            response = ec2_client.describe_instances(
                InstanceIds=[
                    ins_id,
                ],
            )
        except ClientError:
            print('Instance ID not found!')
            sys.exit(0)

        ins_name = response["Reservations"][0]["Instances"][0]["Tags"][0]['Value']
        instance_name.append(ins_name)
    return instance_name


if __name__ == '__main__':
    pass
