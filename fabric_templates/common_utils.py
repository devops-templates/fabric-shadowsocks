#coding=utf-8
from fabric.api import *
from fabric.contrib.files import *

def install():
    sudo('apt-get install -y git')



