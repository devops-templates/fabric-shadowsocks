#coding=utf-8

import os
import tempfile
import json

from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import green as _info

def _sysvinit(action="start"):
    sudo("/etc/init.d/shadowsocks-libev %s" % action)

def install():
    # Only for ubuntu 14.04/16.04
    # sudo("add-apt-repository ppa:max-c-lv/shadowsocks-libev")
    sudo("apt-get update")
    sudo("apt install shadowsocks-libev")

def config(port, passwrod, method="aes-256-cfb",
        obfs_opts="obfs=http;obfs-host=www.baidu.com"):
    template = dict(server="0.0.0.0",
            server_port=port,
            password=password,
            timeout=60,
            method=method,
            obfs_opts=obfs_opts)
    local_path = tempfile.mktemp('.json')
    with open(local_path, 'w+') as outputfile:
        outputfile.write(json.dumps(template, sort_keys=True,
            indent=4, separators=(',', ': ')))
    remote_path = "/etc/shadowsocks-libev/config.json"
    print _info("Uploading config ...\n")
    put(local_path, remote_path, use_sudo=True)
    sudo('chown root: /etc/shadowsocks-libev/config.json')

def start():
    _sysvinit()

def restart():
    _sysvinit('restart')

def stop():
    _sysvinit('stop')

def status():
    _sysvinit('status')

