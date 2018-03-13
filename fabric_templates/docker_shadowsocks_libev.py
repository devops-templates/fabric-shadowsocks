#coding=utf-8
import os
import tempfile
import json

from fabric.api import *
from fabric.contrib.files import *

docker_compose_config="""
version: '2'
services:
  shadowsocks:
    image: xiocode/shadowsocks-libev
    ports:
      - {1}:8388/tcp
      - {1}:8388/udp
    environment:
      - METHOD="{2}"
      - PASSWORD="{0}"
      - OBFS_OPTS="obfs=http;obfs-host=www.bing.com"
    restart: always
"""

def install():
    with cd('~'):
        sudo("git clone https://github.com/devops-templates/docker-shadowsocks-libev.git shadowsocks")

def config(password="1234567890", port=10010, method="aes-192-cfb"):
    with cd('~/shadowsocks'):
        conffile_content = docker_compose_config.format(password, port, method)
        with open('docker-compose.yml', 'w') as confile:
            confile.write(conffile_content)

def up():
    with cd('~/shadowsocks'):
        sudo('docker-compose up -d')



