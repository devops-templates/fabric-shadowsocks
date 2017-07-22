#coding=utf-8
import os
import json
from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import green as _info

def _systemd(action="start"):
    sudo("systemctl %s kcptund" % action)

def install(tarball='https://github.com/xtaci/kcptun/releases/download/v20170525/kcptun-linux-amd64-20170525.tar.gz'):
    print _info("Downloading %s" % tarball)
    filename = os.path.basename(tarball)
    sudo("mkdir -p /opt/kcptun/bin /opt/kcptun/conf && \
            cd /opt/kcptun/bin  && \
            wget %s && \
            tar -zxvf %s && \
            rm -f kcptun-* \
            && chown -R root:root ./*" % (tarball, filename))

def config(listen, target, key,
        crypt="none", mtu="1200", mode="normal",
        args="--nocomp --dscp 46"):
    config_template = dict(listen=listen,
            target=target,
            key=key,
            crypt=crypt,
            mtu=mtu,
            mode=mode)
    local_config_path = tempfile.mktemp('.json')
    with open(local_config_path, 'w+') as conffile:
        conffile.write(json.dumps(config_template, sort_keys=True,
            indent=4, separators=(',', ': ')))

    cmd_template = """
#!/bin/bash -

/opt/kcptun/bin/server_linux_amd64 -c /opt/kcptun/conf/config.json {{args}}

"""
    local_cmd_path = tempfile.mktemp('.sh')
    with open(local_cmd_path, 'w+') as cmdfile:
        cmdfile.write(cmd_template)

    remote_cmd_path = "/opt/kcptun/bin/kcptund"
    upload_template(local_cmd_path, remote_cmd_path,
            dict(args=args),
            use_jinja=True, use_sudo=True, mode="755")

    remote_config_path = "/opt/kcptun/conf/config.json"
    put(local_config_path, remote_config_path, use_sudo=True, mode="644")

def config_systemd():
    sevice_template = """
[Unit]
Description=Kcptund
After=syslog.target
After=network.target

[Service]
Type=simple
User=nobody
Group=nogroup
ExecStart=/opt/kcptun/bin/kcptund
Restart=always

[Install]
WantedBy=multi-user.target
"""
    local_service_path = tempfile.mktemp('.service')
    with open(local_service_path, 'w+') as servicefile:
        servicefile.write(service_template)
    upload_template(local_service_path, "/etc/systemd/system", use_sudo=True)
    sudo("systemctl enable kcptund")

def start():
    _systemd()

def restart():
    _systemd('restart')

def stop():
    _systemd('stop')
