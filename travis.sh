#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSIONS=(3.6.1 3.5.3 3.4.6 3.3.6 3.2.6 3.1.5 3.0.1 2.7.13 2.6.9 2.5.6)

if [ ! -d "$HOME/.pyenv" ] || [ -z "$(ls "$HOME/.pyenv")" ]; then
  git clone https://github.com/pyenv/pyenv.git "$HOME/.pyenv"
fi

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

for version in "${PYTHON_VERSIONS[@]}"; do
  LC_ALL=C.UTF-8 pyenv install -s "$version"
done

pyenv global "${PYTHON_VERSIONS[@]}"
# Have to pin coverage to the same version used by tox, otherwise the
# file format changes.
pip install coverage==4.4.1 tox==2.7.0 virtualenv==13.1.2

tox
