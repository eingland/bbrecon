## Install requirements as admin

pip install -U python-digitalocean paramiko python-dotenv 

## configure .env file

Use .env.example for list of variables to set. SSH password is optional.

## Run build

python build.py

## Running Amass

amass enum -d example.com -config /root/config.ini -o subdomains.txt

## Resources

Based on https://www.trenchesofit.com/2021/06/14/bug-bounty-vps-build/