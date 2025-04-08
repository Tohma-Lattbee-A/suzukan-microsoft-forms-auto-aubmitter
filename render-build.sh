#!/bin/bash

mkdir -p .render/chrome
cd .render/chrome

# Google Chrome をダウンロード
curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 解凍
dpkg -x google-chrome-stable_current_amd64.deb .

# パスを確認
echo "Chrome binary located at:"
echo "$(pwd)/opt/google/chrome/chrome"
