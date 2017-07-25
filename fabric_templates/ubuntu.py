#coding=utf-8
import tempfile

from fabric.api import *
from fabric.contrib.files import *

def _read_pubkey(pubkey_filepath='server-ssh-key.pub'):
    with open(pubkey_filepath, 'r') as f:
        return f.read()

def addgroup(group='fabric-sudoers'):
    run('groupadd %s' % group)
    config = "%%%s ALL=(ALL:ALL) NOPASSWD:ALL" % group
    local_path = tempfile.mktemp('.sudoers')
    with open(local_path, 'w+') as outputfile:
        outputfile.write(config)
    remote_path = "/etc/sudoers.d/10fabric-sudoers"
    put(local_path, remote_path, mode="0440")

def adduser(username='sa', group='fabric-sudoers'):
    run('useradd -m -p "`cat /dev/urandom | head -1 | base64 | head -c 48`" %s' % username)
    run('usermod -a -G "%s" %s' % (group, username))

def config_sshd():
    run('sed -i.bak -e "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config')
    run('sed -e "s/#AuthorizedKeysFile/AuthorizedKeysFile/" /etc/ssh/sshd_config')
    run('sed -e "s/PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config')
    run('sed -e "s/UsePAM yes/UsePAM no/" /etc/ssh/sshd_config')
    run('/etc/init.d/ssh restart')

def config_apt():
    run('echo \'Acquire::ForceIPv4 "true";\' > /etc/apt/apt.conf.d/99force-ipv4')

def upload_pubkey(username='sa', pubkey_filepath='server-ssh-key.pub'):
    ssh_dir = '/home/%s/.ssh' % username
    auth_keys_filepath = '%s/authorized_keys' % ssh_dir
    run('mkdir -p %s' % ssh_dir)
    run('touch %s' % auth_keys_filepath)
    run('chmod 600 %s' % auth_keys_filepath)
    run('chown -R %s: %s' % (username, ssh_dir))
    append(auth_keys_filepath, _read_pubkey(pubkey_filepath))

def init():
    adduser()
    addgroup()
    upload_pubkey()
    config_apt()
    config_sshd()

