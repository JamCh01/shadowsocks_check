# shadowsocks_check
You can check your SS server status by this script. And it will be the most graceful way.

## how to install it

You should install shadowsocks-libev first. You can find how to install it [here.](https://github.com/shadowsocks/shadowsocks-libev#installation)

clone this project and install
```
git clone git@github.com:JamCh01/shadowsocks_check.git
cd shadowsocks_check
python3 setup.py install
```

or use pypi
```
pip3 install shadowsocks_check
```

*BTW, Python3 only and doesn't support WSL.*

## how to use it

there are some supported arguments.
```
ss-check
--threads             the number of threads
--start_port          start port range, range(start_port, start_port+threads)
--config              shadowsocks config file
--mode                ss or ssr (fake now)
```