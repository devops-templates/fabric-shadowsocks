#coding=utf8

import tempfile

from fabric.api import *
from fabric.contrib.files import *

monitrc = """
set daemon 120
set logfile /var/log/monit.log
set idfile /var/lib/monit/id
set statefile /var/lib/monit/state
set eventqueue
    basedir /var/lib/monit/events
    slots 100
set httpd port 2812 and
    use address localhost
    allow localhost
    allow admin:monit
include /etc/monit/conf.d/*
"""

monit="""check process user-{0} with pidfile /opt/shadowsocks/user-{0}/shadowsocks.pid
    start program = "/opt/shadowsocks/user-{0}/ssserver start"
    stop program = "/opt/shadowsocks/user-{0}/ssserver stop"
"""

ssserver="""#!/bin/bash
PID=/opt/shadowsocks/user-{0}/shadowsocks.pid
LOG=/opt/shadowsocks/user-{0}/shadowsocks.log

function start_app {{
    nohup ss-server -s 0.0.0.0 -p {0} -k {1} -m {2} 1>>"$LOG" 2>&1 &
    echo $! > "$PID"
}}

function stop_app {{
    if ps -p `cat $PID` > /dev/null
    then
        kill `cat $PID`
    fi
}}

case $1 in
    start)
        start_app ;;
    stop)
        stop_app ;;
    restart)
        stop_app
        start_app
        ;;
    *)
        echo "usage: ssserver [start|stop|restart]" ;;
esac
exit 0

"""


def install():
    sudo("apt-get update")
    sudo("apt install software-properties-common monit -y")
    sudo("add-apt-repository ppa:max-c-lv/shadowsocks-libev -y")
    sudo("apt-get update")
    sudo("apt install shadowsocks-libev -y")


def config(ports='8080-8090', passwd='nopasswd', method="aes-256-cfb"):
    # config monit
    remote_monitrc = '/etc/monit/monitrc'
    local_monitrc = tempfile.mktemp('.conf')
    with open(local_monitrc, 'w') as f:
        f.write(monitrc)
    put(local_monitrc, remote_monitrc, use_sudo=True, mode="600")
    sudo('chown root:root %s' % remote_monitrc)

    # make monit auto start
    sudo("systemctl enable monit")

    # user config
    ports = ports.split('-')
    for port in xrange(int(ports[0]), int(ports[1]) + 1):
        # mkdir
        workdir = '/opt/shadowsocks/user-%s' % port
        sudo('mkdir -p %s' % workdir)

        # write ssserver
        remote_ssserver = '%s/ssserver' % workdir
        local_ssserver = tempfile.mktemp('.sh')
        content = ssserver.format(port, passwd, method)
        with open(local_ssserver, 'w') as f:
            f.write(content)
        put(local_ssserver, remote_ssserver, use_sudo=True, mode="755")

        # write monit conffile
        remote_monit = '%s/monit.conf' % workdir
        local_monit = tempfile.mktemp('.conf')
        content = monit.format(port, passwd, method)
        with open(local_monit, 'w') as f:
            f.write(content)
        put(local_monit, remote_monit, use_sudo=True, mode="644")

        # clear solf link is exist
        sudo('rm -f /etc/monit/conf.d/user-%s.conf' % port)

        # make soft link
        sudo('ln -s %s/monit.conf /etc/monit/conf.d/user-%s.conf' % (workdir, port))


def start():
    sudo('monit reload')

