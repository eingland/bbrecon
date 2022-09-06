#!/bin/bash
#Script to check subdomains.txt every hour and upload if new items have been added
while true; do echo subdomains.txt | /root/go/bin/anew | aws s3 cp subdomains.txt s3://TrenchesofITS3/ ; sleep 3600 ; done