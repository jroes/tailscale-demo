#!/bin/bash

# Inspired by https://github.com/QuinnyPig/tailscale-layer/blob/main/extension1.sh

./tailscaled --tun=userspace-networking --socket=/tmp/tailscale.sock --state /tmp/tailscale &
./tailscale --socket=/tmp/tailscale.sock up --authkey=$KEY
