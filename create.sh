#!/bin/bash

set -euo pipefail

cd ansible
ansible-playbook playbooks/create.yml -i inventory/hosts.ini --vault-password-file vault-pwd.txt -K
cd ..
