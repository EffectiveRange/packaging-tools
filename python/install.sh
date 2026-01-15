#!/bin/bash

# Install dependencies
apt-get update

# Install python3 and pip
apt-get install -y --no-install-recommends python3-all python3-pip python3-virtualenv python3-wheel python3-build

# Install fpm
apt-get install -y --no-install-recommends ruby ruby-dev rubygems build-essential
gem install -N fpm

# Install stdeb
apt-get install -y --no-install-recommends debhelper devscripts equivs dh-python python3-stdeb

# Install dh-virtualenv
apt-get install -y --no-install-recommends dh-virtualenv

# Add scripts to PATH
SCRIPTS_DIR=$(dirname "$0")
ABSOLUTE_SCRIPTS_DIR=$(cd "$SCRIPTS_DIR" && pwd)

find "$ABSOLUTE_SCRIPTS_DIR" -maxdepth 1 -name "pack_*" | while read -r script_path
do
  script_name=$(basename "$script_path")
  ln -svf "$script_path" "/usr/local/bin/$script_name"
done
