#!/bin/bash

if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments"
  exit 2
fi

HOST=$1
echo "Installing CoinTicker on host $HOST"
ansible-playbook -u pi -i $HOST, setup.yml --ask-pass
