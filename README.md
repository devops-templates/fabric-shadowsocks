# fabric-templates

fabric templates for ubuntu 14.04+

## Templates

Including:

* frp
* kcptun
* shadowsocks-libev
* bbr(x86_64)

## Usage

### Install fabric 

```
pip install fabric
```

### Write a `fabfile.py`

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
```

