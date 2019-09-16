from __future__ import print_function
import time
import paramiko
import logging

SSH_KEY_PATH = '/Users/ksd/.ssh/id_rsa'


def connection(ip, ssh_username, seconds):
    for _ in range(40):
        if seconds:
            time.sleep(seconds)
        else:
            time.sleep(5)
        try:

            private_key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(hostname=ip,
                        username=ssh_username,
                        password='',
                        pkey=private_key)
            # The issue can solve 'SSH session not active'  https://github.com/paramiko/paramiko/issues/928
            if ssh.get_transport().active:
                logging.info(f'Connection instance succeeded!')
                break
        except:
            ssh.close()
    return ssh


def executor(client, command, seconds=300):
    assert (client and command is not None)
    stdin, stdout, stderr = client.exec_command(command, timeout=seconds)
    result = stdout.read().decode('utf-8')
    # result = res if res else err
    return result
