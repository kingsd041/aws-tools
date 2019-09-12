# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import logging
import ksd


def main():
    """Exercise create_ec2_instance()"""

    ins_name = input('实例名称: ')
    ins_count = input('实例个数 [1]: ')
    ins_type = input('实例类型: \n'
                     't2.small  -- 1C2G \n'
                     't2.medium -- 2C4G \n'
                     'c5.xlarge -- 4C8G \n'
                     '更多请参考: https://aws.amazon.com/cn/ec2/instance-types/ \n'
                     '[t2.small]\n: ')
    ins_image_id = input('镜像ID:\n'
                         'ami-0d0eaed20348a3389 -- Ubuntu1804 \n'
                         'ami-0080c730c4da27081 -- Windows 2019 Container\n'
                         '[ami-0d0eaed20348a3389 -- Ubuntu1804]\n:')
    ins_disk_size = input('磁盘大小 [8]: ')

    install_docker = input('是否安装docker [y/n]: ')


    min_count = int(ins_count if ins_count is not '' else 1)
    max_count = min_count
    instance_type = ins_type if ins_type is not '' else 't2.small'
    image_id = ins_image_id.strip() if ins_image_id is not '' else 'ami-0d0eaed20348a3389'
    volume_size = int(ins_disk_size.strip()) if ins_disk_size is  not '' else 8

    instance_name = ins_name.strip()
    keypair_name = 'hailong'

    security_group = ['default']
    block_device_mapping = [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': volume_size
            },

        },

    ]

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Provision and launch the EC2 instance
    instance_info = ksd.create_ec2_instance(image_id=image_id,
                                            instance_type=instance_type,
                                            keypair_name=keypair_name,
                                            min_count=min_count,
                                            max_count=max_count,
                                            security_group=security_group,
                                            block_device_mapping=block_device_mapping)
    print(instance_info)
    if instance_info is not None:
        logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
        logging.info(f'    Current State: {instance_info["State"]["Name"]}')

    # Create the tag for the instance
    tags_info = ksd.create_instance_tags(instance_info["InstanceId"], 'Name', instance_name)
    print(tags_info)

    if install_docker == 'Y' or install_docker == 'y':
        instance_public_ip = ksd.get_instance_public_ip(instance_info["InstanceId"])
        result = ksd.install_docker(instance_public_ip)
        assert 'Server: Docker Engine - Community' in result, 'Install docker failed!'

if __name__ == '__main__':
    main()
