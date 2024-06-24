#!/bin/bash
set -eu

BLENDER="${1:-}"
PYTHON="${2:-}"

if [ -z "$BLENDER" ] || [ -z "$PYTHON" ]; then
 echo "$0 <Blender Version> <Python Version>" >&2
 exit 1
fi

VENV=".venv"
if [ -n "$WINDIR" ]; then
   ACTIVATE="Scripts/activate"
else
   ACTIVATE="bin/activate"
fi

cd $(dirname $0)
if ! pyenv versions | grep -q "$PYTHON"; then
  echo "Install Python $PYTHON"
  pyenv install "$PYTHON"
fi
pyenv local "$PYTHON"

if [ ! -d $VENV ];then
  python -m venv $VENV
  source $VENV/$ACTIVATE
  pip install fake-bpy-module-$BLENDER
else
  source $VENV/$ACTIVATE
fi

mkdir -p .vscode
cat << EOF > .vscode/settings.json
{
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/Thumbs.db": true,
    ".venv/": true,
    ".python-version": true
  }
}
EOF

echo ""
echo " Run: 'source ./$VENV/$ACTIVATE' to activate the virtual environment"
echo ""
