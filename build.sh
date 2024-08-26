#!/bin/bash -ex

SCRIPTS_DIR=$(dirname "$0")
ABSOLUTE_SCRIPTS_DIR=$(cd "$SCRIPTS_DIR" && pwd)

cd "$ABSOLUTE_SCRIPTS_DIR"
rm -rf dist
mkdir dist

find "$ABSOLUTE_SCRIPTS_DIR" -maxdepth 2 -name "pack_*" | while read -r script_path
do
  script_name=$(basename "$script_path")
  cp -v "$script_path" "dist/$script_name"
done

cd dist
tar -cvzf packaging-tools.tar.gz ./*

cd "$ABSOLUTE_SCRIPTS_DIR"
rm -rf debian/usr/local/bin
mkdir -p debian/usr/local/bin

cp -v dist/pack_* debian/usr/local/bin

VERSION="$(grep Version: debian/DEBIAN/control | cut -d' ' -f2)"

dpkg-deb -Zxz --root-owner-group --build debian "dist/packaging-tools_$VERSION-1_all.deb"
