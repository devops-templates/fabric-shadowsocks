#coding=utf-8
import os
import json
import tempfile

from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import green as _info

def _systemd(action="start"):
    sudo("systemctl %s telegraf" % action)

def install(package='https://dl.influxdata.com/telegraf/releases/telegraf_1.3.4-1_amd64.deb'):
    print _info("Downloading %s" % package)
    filename = os.path.basename(package)
    with cd("/tmp"):
        run("wget %s" % package)
        sudo("dpkg -i %s" % filename)

def start():
    _systemd()

def restart():
    _systemd("restart")

def stop():
    _systemd("stop")

def status():
    _systemd("status")


