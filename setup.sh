#!/bin/bash

set -e

sudo apt update -y

sudo apt install sshpass -y
sudo apt install ansible -y

ssh-keygen -b 4096 -t rsa -f ~/.ssh/rpi -N "" <<< y

read -p "Enter Raspberry Pis initial IP address: " IP_ADDRESS

cd ansible
ansible-playbook --user pi --ask-pass --inventory $IP_ADDRESS',' playbooks/setup-password.yml
ansible-playbook --user pi --ask-pass --inventory $IP_ADDRESS',' playbooks/setup-lockdown.yml
cd ..
