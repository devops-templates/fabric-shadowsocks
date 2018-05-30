# fabric-templates

fabric templates for ubuntu 16.04

## Templates

Including:

* ubuntu (only allow authkey to login)
* docker-ce
* docker-compose
* frp
* kcptun
* docker_shadowsocks-libev
* bbr(x86_64)
* grafana
* telgraf
* influxdb

## Usage

### Install fabric 

```
pip install fabric
```

### [OPTION] Write a `fabfile.py`

```
from fabric_templates.kcptun import *
```

### Run the command via fabric
```
(ball) ➜  fabric-templates fab -l
Available commands:

    config
    config_systemd
    install
    restart
    start
    stop

# OR

(ball) ➜  fabric-templates git:(master) ✗ fab -f fabric_templates/kcptun.py -l
```

### Install SS on GCP

```
(ball) ➜  ~ fab -i ~/.ssh/vps-ssh-key -H sa@YOUT_SERVER_IP -f gcp.py setup:port=10018,password=<Your Password>

```

### Install SS on vulr

```
(ball) ➜  ~ fab -H root@YOUT_SERVER_IP -f vulr.py setup

```
