#coding=utf8

from fabric_templates import bbr
from fabric_templates import common_utils
from fabric_templates import docker_ce
from fabric_templates import docker_compose
from fabric_templates import docker_shadowsocks_libev

def install():
    common_utils.install()
    docker_ce.install()
    docker_compose.install()
    docker_shadowsocks_libev.install()

def config(password='YxjGRdC3o9LWQJyp'):
    bbr.config()
    docker_shadowsocks_libev.config(password)

def start():
    docker_shadowsocks_libev.up()

def setup():
    install()
    config()
    start()


