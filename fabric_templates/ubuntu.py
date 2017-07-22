#coding=utf-8
from fabric.api import *
from fabric.contrib.files import *

def _read_pubkey(pubkey_filepath='vps-ssh-key.pub'):
    with open(pubkey_filepath, 'r') as f:
        return f.read()

def adduser(username='sa'):
    run('useradd -m -p "`cat /dev/urandom | head -1 | base64 | head -c 48`" %s' % username)
    run('usermod -a -G sudo %s' % username)
    run('chmod 640 /etc/sudoers')
    append('/etc/sudoers', '%s      ALL=(ALL) NOPASSWD: ALL' % username)
    run('chmod 440 /etc/sudoers')

def config_sshd():
    run('sed -i -e "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config')
    run('sed -i -e "s/#AuthorizedKeysFile/AuthorizedKeysFile/" /etc/ssh/sshd_config')
    run('sed -i -e "s/PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config')
    run('sed -i -e "s/UsePAM yes/UsePAM no/" /etc/ssh/sshd_config')
    run('/etc/init.d/ssh restart')

def config_apt():
    run('echo \'Acquire::ForceIPv4 "true";\' > /etc/apt/apt.conf.d/99force-ipv4')

def upload_pubkey(username='sa', pubkey_filepath='vps-ssh-key.pub'):
    ssh_dir = '/home/%s/.ssh' % username
    auth_keys_filepath = '%s/authorized_keys' % ssh_dir
    run('mkdir -p %s' % ssh_dir)
    run('touch %s' % auth_keys_filepath)
    run('chmod 600 %s' % auth_keys_filepath)
    run('chown -R %s: %s' % (username, ssh_dir))
    append(auth_keys_filepath, _read_pubkey(pubkey_filepath))

