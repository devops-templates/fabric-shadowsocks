# fabric-templates

fabric templates for ubuntu 16.04

## Templates

Including:

* docker_shadowsocks-libev
* docker-ce
* docker-compose
* shadowsocks-libev
* bbr(x86_64)
* ubuntu (only allow authkey to login)

## Usage

### Install fabric 

```
pip install 'fabric<2.0'
```

## Native

```
fab -H sa@ip -f fabric_templates/shadowsocks_libev.py install config:ports=9000-9010,passwd=kingking,method=aes-192-cf start

```

## Using docker

### Install SS on Google Cloud

```
fab -i ~/.ssh/vps-ssh-key -H sa@ip -f gcp.py setup:port=10018,password=<Your Password>

```

### Install SS on vulr

```
fab -H sa@ip -f vulr.py setup

```

