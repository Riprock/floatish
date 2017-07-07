#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if [ ! -d "$HOME/.pyenv" ]; then
  curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"' >> "$HOME/.bash_profile"
  . "$HOME/.bash_profile"
  pyenv install 2.7.13
  pyenv install 3.0.1
  pyenv install 3.1.5
  pyenv install 3.2.6
  pyenv install 3.3.6
  pyenv install 3.4.6
  pyenv install 3.5.3
  pyenv install 3.6.1
else
  ls "$HOME/.pyenv"
fi
