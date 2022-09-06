# Based on https://www.trenchesofit.com/2021/06/14/bug-bounty-vps-build/

import digitalocean
import random
import time
import paramiko
from dotenv import load_dotenv
import os

load_dotenv()

dokey = os.getenv('token')
password = os.getenv('password')
pathToSSHKey = os.getenv('pathToSSHKey')

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
manager = digitalocean.Manager(token=dokey)
key = manager.get_all_sshkeys()


def createDroplet(number):
    print("[+] Creating new droplet...")
    droplet = digitalocean.Droplet(token=manager.token,
                                   name='bugbounty' + str(number),
                                   region='nyc3',
                                   image='ubuntu-22-04-x64',
                                   size_slug='s-1vcpu-1gb',
                                   ssh_keys=key,
                                   backups=False)
    droplet.create()
    complete()


def deleteAllDroplets():
    print("[+] Removing all droplets...")
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.destroy()
        complete()


def randomDropletName():
    number = random.randint(1, 1000)
    return number


def getIP():
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        data = droplet.load()
        publicIP = data.ip_address
        return publicIP


def executeBuild():
    stdin, stdout, stderr = ssh_client.exec_command('chmod +x build.sh')
    print(stdout.readline())
    stdin, stdout, stderr = ssh_client.exec_command('bash /root/build.sh')
    print(stdout.readline())
    time.sleep(600)
    complete()


def moveFiles():
    sftp_client = ssh_client.open_sftp()
    # VPS Build Script
    sftp_client.put('build.sh', 'build.sh')
    # Amass config
    sftp_client.put('config.ini', 'config.ini')
    # AWS config
    sftp_client.put('.aws.zip', '.aws.zip')
    # AWS Upload Script
    sftp_client.put('awsupload.sh', 'awsupload.sh')
    # AWS Upload Service
    sftp_client.put('awsupload.service', 'awsupload.service')
    sftp_client.close()
    sftp_client.close()
    complete()


def complete():
    print("[+] Complete")


deleteAllDroplets()
createDroplet(randomDropletName())
print("[+] Getting instance information...")
time.sleep(30)
ip = getIP()
ssh_client.connect(hostname=ip, username='root', password=password,
                   key_filename=pathToSSHKey)
print("[+] Waiting for sshd to start...")
time.sleep(60)
print("[+] Moving needed files to target server...")
moveFiles()
print("[+] Executing commands...")
executeBuild()
