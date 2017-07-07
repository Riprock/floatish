#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

PYTHON_VERSIONS='3.6.1 3.5.3 3.4.6 3.3.6 3.2.6 3.1.5 3.0.1 2.7.13'

install_python_versions=0

if [ ! -d "$HOME/.pyenv" ] || [ -z "$(ls $HOME/.pyenv)" ]; then
  install_python_versions=1
  git clone https://github.com/pyenv/pyenv.git "$HOME/.pyenv"
fi

echo 'export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"' >> "$HOME/.bash_profile"
. "$HOME/.bash_profile"

if [ "$install_python_versions" = "1" ]; then
  for version in $PYTHON_VERSIONS; do
    pyenv install "$version"
  done
fi

pyenv global $PYTHON_VERSIONS
# Have to pin coverage to the same version used by tox, otherwise the
# file format changes.
pip install coverage==4.4.1 python-coveralls==2.9.1 tox==2.7.0 virtualenv==13.1.2
