# run-aws-instance

## 说明
- 目前只支持`ca-central-1` region, 和一些只适合本人的特殊配置，在您的环境上使用，还需要修改 `image_id` `security_group` `keypair_name` `region` 等参数
- 只支持python3
- 使用请配置 `~/.aws/config`
## 如何使用



```
# git clone https://github.com/kingsd041/aws-tools.git
# mv aws-tools aws
```


```
 ksd@Hailong-MacBook-Pro  /usr/local/bin  cat ksd-launch-aws-instance
#!/bin/bash

python3 ~/aws/create_instance.py
 ksd@Hailong-MacBook-Pro  /usr/local/bin  cat ksd-list-instances
#!/bin/bash

python3 ~/aws/ksd_list_instances.py
 ksd@Hailong-MacBook-Pro  /usr/local/bin  cat ksd-terminate-all-instances
#!/bin/bash

python3 ~/aws/ksd_terminate_all_instances.py
 ksd@Hailong-MacBook-Pro  /usr/local/bin  cat ksd-terminate-instances
#!/bin/bash

python3 /Users/ksd/aws/ksd_terminate_instances.py $1 $2 $3 $4 $5 $6 $7 $8
```
