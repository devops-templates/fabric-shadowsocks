# fabric-shadowsocks

shadowsocks fabric templates for ubuntu 16.04

## Templates

Including:

* shadowsocks-libev
* bbr(x86_64)
* ubuntu (only allow authkey to login)

## Usage

### Install fabric 

```
pip install 'fabric<2.0'
```

## Install

```
fab -H root@your_vps_ip \
-f fabric_templates/shadowsocks_libev.py \
install \
config:ports=9000-9010,passwd=kingking,method=aes-192-cfb \
start

```

## Re-Config


```
fab -H root@your_vps_ip \
-f fabric_templates/shadowsocks_libev.py \
provision \
config:ports=9000-9010,passwd=kingking,method=aes-192-cfb \
start

```

## Install and Config  BBR

```
fab -H root@your_vps_ip -f fabric_templates/bbr.py upgrade_kernel

# After reboot

fab -H root@your_vps_ip -f fabric_templates/bbr.py config
```

## Enable IPv4 Only for apt

```
fab -H root@your_vps_ip -f fabric_templates/ubuntu.py apt_config
```
