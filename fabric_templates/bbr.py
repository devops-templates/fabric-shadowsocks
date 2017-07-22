#coding=utf-8
from fabric.api import *
from fabric.contrib.files import *

def upgrade_kernel(deburl='http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.12.2/linux-image-4.12.2-041202-generic_4.12.2-041202.201707150832_amd64.deb'):
    with cd('/tmp'):
        run('wget %s' % deburl)
        sudo('dpkg -i linux-image-4.*.deb')
        sudo('update-grub')
        sudo('reboot')

def config():
    sudo('modprobe tcp_bbr')
    sudo('sh -c \'echo "tcp_bbr" >> /etc/modules-load.d/modules.conf\'')
    sudo('sh -c \'echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf\'')
    sudo('sh -c \'echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf\'')
    sudo('sysctl -p')
    sudo('sysctl net.ipv4.tcp_available_congestion_control')
    sudo('sysctl net.ipv4.tcp_congestion_control')

