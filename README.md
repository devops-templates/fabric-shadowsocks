# fabric-templates

fabric templates for ubuntu 14.04+

## Templates

Including:

* ubuntu (only allow authkey to login)
* docker-ce
* docker-compose
* frp
* kcptun
* shadowsocks-libev
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

