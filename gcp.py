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

def enable_bbr():
    bbr.config()

def config(port, password):
    docker_shadowsocks_libev.config(port, password)

def start(port):
    docker_shadowsocks_libev.up(port)

def restart(port):
    docker_shadowsocks_libev.restart(port)

def setup(port="10090", password="ubUAOMdPisCG9v26"):
    config(port, password)
    start(port)


