#!/usr/bin/env bash
set -e

echo "[+] Building VPS bug bounty server"

echo "[+] Updating Packages"
apt-get -y update && apt-get -y upgrade

echo "[+] Installing unzip"
apt-get -y install unzip

echo "[+] Installing git"
apt-get install git

echo "[+] Installing tmux"
apt-get install tmux

echo "[+] Installing go"
wget https://golang.org/dl/go1.16.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
cp /usr/local/go/bin/go /bin/go
go version

echo "[+] Installing NMAP"
apt-get -y install nmap

echo "[+] Installing anew"
go get -u github.com/tomnomnom/anew

echo "[+] Installing waybackurls"
go get github.com/tomnomnom/waybackurls

echo "[+] Installing massdns"
git clone https://github.com/blechschmidt/massdns.git

echo "[+] Installing gobuster"
apt-get -y install gobuster

echo "[+] Installing ffuf"
go get -u github.com/ffuf/ffuf

echo "[+] Bypass 403 pull"
git clone https://github.com/iamj0ker/bypass-403
chmod +x /root/bypass-403/bypass-403.sh

echo "[+] SecLists pull"
git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/

echo "[+] Installing amass"
sudo snap install amass

echo "[+] Installing aws cli"
apt-get -y install awscli
unzip /root/.aws.zip -d /root/

touch subdomains.txt

echo "[+] Configuring AWS upload service"
chmod +x /root/awsupload.sh
mv /root/awsupload.service /etc/systemd/system/awsupload.service

echo "[+] Starting AWS upload service"
systemctl enable uploadscript.service
systemctl start uploadscript.service

echo "[+] Configuring hostname"
hostnamectl set-hostname bbrecon
cat << EOF > /etc/hosts
127.0.0.1 localhost
127.0.0.1 bbrecon
EOF

echo "[+] Cleaning up"
rm -rf /root/buildscript.sh
find /var/log -type f -exec sh -c "cat /dev/null > {}" \;