#!/bin/bash

while true; do
    git pull
    python3 inline_bot.py
    sleep 1
done
