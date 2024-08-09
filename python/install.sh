#!/bin/bash

# Install dependencies
apt-get update

# Install python3 and pip
apt-get install -y --no-install-recommends python3 python3-pip

# Install wheel
pip3 install wheel

# Install fpm
apt-get install -y --no-install-recommends ruby ruby-dev rubygems build-essential
gem install -N fpm

# Install dh-virtualenv and stdeb
apt-get install -y --no-install-recommends debhelper devscripts equivs dh-virtualenv dh-python python3-virtualenv python3-all
pip3 install stdeb

# Add scripts to PATH
SCRIPTS_DIR=$(dirname "$0")

find "$SCRIPTS_DIR" -name "pack_*" | while read -r script_path
do
  script_name=$(basename "$script_path")
  ln -svf "$script_path" "/usr/local/bin/$script_name"
done
