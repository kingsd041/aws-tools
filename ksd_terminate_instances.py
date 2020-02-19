import aws_tools
import sys

instances_list = sys.argv[1:]
if not instances_list:
    print(' usage: ksd-terminate-instances [instance id] ... \n')
    sys.exit(0)

instances_name = aws_tools.instance_id_conversion_name(instances_list)
aws_tools.terminate_instances_custom(instances_list, instances_name)
