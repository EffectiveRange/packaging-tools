#!/bin/bash
cd $(dirname $0)
rm -rf dist
mkdir dist

IGNORE_EXT="cfg|md"

for stacks in $(find  . -maxdepth 1 -type d  ! -name '.*' ! -name 'dist')
do
    for files in $(find  $stacks -maxdepth 1 -type f  | grep -vE "\.($IGNORE_EXT)$")
    do
        cp -v $files dist/
    done
done

cd dist
tar -cvzf packaging-tools.tar.gz ./*