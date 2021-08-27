import aws_tools
import sys

instances_list = sys.argv[1:]
if not instances_list:
    print(' usage: ksd_add_instance_tags [instance id] ... \n')
    sys.exit(0)

for instace in instances_list:
    instances_name = aws_tools.instance_id_conversion_name_1(instace)
    aws_tools.create_instance_tags(instace, "DoNotDelete", "true")
    aws_tools.create_instance_tags(instace, "Owner", "hailong")
    print(' Instance ' +instances_name+' tag added successfuly !')
