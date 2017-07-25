#coding=utf-8
from fabric.api import *
from fabric.contrib.files import *

def install(version='1.14.0'):
    sudo("curl -L https://github.com/docker/compose/releases/download/%s/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose" % version)
    sudo("chmod +x /usr/local/bin/docker-compose")

