#coding=utf-8

import os

from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import green as _info

def install():
    # Uninstall old versions
    sudo("apt-get remove docker docker-engine docker.io")
    sudo("apt-get update")
    # Only for ubuntu 14.04
    # sudo("apt-get install -y \
    #        linux-image-extra-$(uname -r) \
    #        linux-image-extra-virtual")
    sudo("apt-get install -y \
            apt-transport-https \
            ca-certificates \
            curl \
            software-properties-common")
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
    sudo("apt-key fingerprint 0EBFCD88")
    sudo('add-apt-repository \
            "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) \
            stable"')
    sudo("apt-get update")
    sudo("apt-get install -y docker-ce")

