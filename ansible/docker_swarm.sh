#!/bin/bash
. ./openrc.sh; ansible-playbook -i inventory/hosts.ini --ask-become-pass docker_swarm.yaml