#!/bin/bash
set -eu
########################################
# Addon Name
addon=""
########################################
cd $(dirname $0)
# if addon is empty, set it to the project directory name
if [ -z "$addon" ];then
  addon=$(basename $(pwd))
fi

# check src directory
if [ ! -d $addon ];then
  echo "'$(pwd)/$addon' source directory not found." >&2
  ext 1
fi

rm -f $addon.zip
zip -r $addon.zip $addon/*

echo "Generate: '$(pwd)/$addon.zip'"
