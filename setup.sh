#!/bin/bash
echo "Installing all requirements, please wait..."
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install termux-api -y
pip install -r requirements.txt
python nayef_legend.py
