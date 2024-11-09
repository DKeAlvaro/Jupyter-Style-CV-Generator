#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Install TeX Live and required packages
apt-get update
apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra