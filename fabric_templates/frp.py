#coding=utf-8
from fabric.api import *
from fabric.contrib.files import *

def _systemd(action="start"):
    sudo("systemctl %s frpd" % action)

def install(tarball='https://github.com/fatedier/frp/releases/download/v0.12.0/frp_0.12.0_linux_amd64.tar.gz'):
    filename = os.path.basename(tarball)
    sudo("cd /tmp && wget %s && tar -zxvf %s && mv %s /opt/frp && mkdir /opt/frp/bin" % (tarball, filename, filename.replace('.tar.gz', "")))

def config():
    cmd_template = """
#!/bin/bash -

/opt/frp/frps -c /opt/frp/frps.ini

"""
    local_cmd_path = tempfile.mktemp('.sh')
    with open(local_cmd_path, 'w+') as cmdfile:
        cmdfile.write(cmd_template)

    remote_cmd_path = "/opt/frp/bin"
    upload_template(local_cmd_path, remote_cmd_path,
            use_jinja=True, use_sudo=True, mode="755")

def config_systemd():
    sevice_template = """
[Unit]
Description=frpd
After=syslog.target
After=network.target

[Service]
Type=simple
User=nobody
Group=nogroup
ExecStart=/opt/frp/bin/frpd
Restart=always

[Install]
WantedBy=multi-user.target
"""
    local_service_path = tempfile.mktemp('.service')
    with open(local_service_path, 'w+') as servicefile:
        servicefile.write(service_template)
    upload_template(local_service_path, "/etc/systemd/system", use_sudo=True)
    sudo("systemctl enable frpd")

def start():
    _systemd()

def restart():
    _systemd('restart')

def stop():
    _systemd('stop')

