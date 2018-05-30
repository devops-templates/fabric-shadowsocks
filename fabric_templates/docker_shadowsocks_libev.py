#coding=utf-8
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
      - {0}:8388/tcp
      - {0}:8388/udp
    environment:
      - METHOD={1}
      - PASSWORD={2}
      - OBFS_OPTS=obfs=http;obfs-host=www.bing.com
    restart: always
"""

def install(port, password, method="aes-192-cfb"):
    sudo("mkdir -p /opt/shadowsocks/user-%s" % port)

def config(port, password, method="aes-192-cfb"):
    sudo("mkdir -p /opt/shadowsocks/user-%s" % port)
    remote_config_path = '/opt/shadowsocks/user-%s/docker-compose.yml' % port
    local_config_path = tempfile.mktemp('.yml')
    conffile_content = docker_compose_config.format(port, method, password)
    with open(local_config_path, 'w') as confile:
        confile.write(conffile_content)

    put(local_config_path, remote_config_path, use_sudo=True, mode="644")

def up(port):
    with cd('/opt/shadowsocks/user-%s' % port):
        sudo('docker-compose up -d')

def restart(port):
    with cd('/opt/shadowsocks/user-%s' % port):
        sudo('docker-compose restart')


