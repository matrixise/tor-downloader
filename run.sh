#!/usr/bin/fish
env UID=(id -u) GID=(id -g) docker-compose up --scale worker=8 --build
