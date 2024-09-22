#!/bin/zsh
python3 main.py build
cd build/
python3 -m http.server
cd ..
