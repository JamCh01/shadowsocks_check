# shadowsocks_check
You can check your SS server status by this script. And it will be the most graceful way.

## how to install it

You should install shadowsocks-libev first. You can find how to install it [here.](https://github.com/shadowsocks/shadowsocks-libev#installation)

clone this project and install
```
git clone git@github.com:jamcplusplus/shadowsocks_check.git
cd shadowsocks_check
python3 setup.py install
```

*BTW, Python3 Only.*

## how to use it

there are some supported arguments.
```
ss-check
--threads             the number of threads
--start_port          start port range,range(start_port, start_port+threads)
--config              shadowsocks config file
--mode                ss or ssr (fake now)
```