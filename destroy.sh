#!/bin/bash

set -euo pipefail

cd ansible
ansible-playbook playbooks/destroy.yml -i inventory/hosts.ini --vault-password-file vault-pwd.txt -K
cd ..
