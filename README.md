# awesome-shadowsocks-check
You can check your SS server status by this script. And it will be the most graceful way.

## how to install it

You should install shadowsocks-libev first. You can find how to install it [here.](https://github.com/shadowsocks/shadowsocks-libev#installation)

clone this project
```
git clone git@github.com:jamcplusplus/awesome-shadowsocks-check.git
```

install requirements.txt
```
cd awesome-shadowsocks-check
pip3 install -r requirements.txt
```

*BTW, Python3 only and doesn't support WSL.*

## how to use it

You should paste your config file, and must be renamed `gui-config.json`. Then, run it by:
```
python3 awesome-shadowsocks-check.py
```
