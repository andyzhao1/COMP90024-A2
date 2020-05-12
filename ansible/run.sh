#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts --ask-become-pass all-in-one.yaml