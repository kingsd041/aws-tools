import aws_tools
from sys import argv

instances_list = argv[1:]
instances_name = aws_tools.instance_id_conversion_name(instances_list)
aws_tools.terminate_instances_custom(instances_list, instances_name)
