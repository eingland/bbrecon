# https://www.trenchesofit.com/2021/06/14/bug-bounty-vps-build/

import digitalocean
import random
import time
import paramiko

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
manager = digitalocean.Manager(token=$token)
key = manager.get_all_sshkeys()