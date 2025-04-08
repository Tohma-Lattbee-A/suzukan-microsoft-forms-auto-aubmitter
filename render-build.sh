#!/usr/bin/env bash

# Install Chromium manually
mkdir -p .local/chrome
cd .local/chrome

curl -SL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
apt-get update && apt-get install -y ./chrome.deb

# Install chromedriver
cd /opt/render/project/src
pip install -r requirements.txt
