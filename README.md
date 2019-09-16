# run-aws-instance

## 说明
- 目前只支持`ca-central-1` region, 和一些只适合本人的特殊配置，在您的环境上使用，还需要修改 `image_id` `security_group` `keypair_name` `region` 等参数
- 只支持python3
- 使用请配置 `~/.aws/config`
## 如何使用



```
# git clone https://github.com/kingsd041/run-aws-instance.git
# python run-aws-instance/create_instance.py
```