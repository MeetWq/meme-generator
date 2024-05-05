#! /usr/bin/env bash

mkdir -p ~/.config/meme_generator

envsubst < /app/config.toml.template > ~/.config/meme_generator/config.toml

exec python /app/bot.py
