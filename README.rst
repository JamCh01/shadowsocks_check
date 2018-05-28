=================
shadowsocks_check
=================
You can check your SS server status by this script. And it will be the most graceful way.

-----------------
how to install it
-----------------
You should install shadowsocks-libev first. You can find how to install it [here.](https://github.com/shadowsocks/shadowsocks-libev#installation)

`pip3 install shadowsocks_check`


*BTW, Python3 Only.*
-------------
how to use it
-------------
there are some supported arguments.

+------------------------+--------------------------------------+                     
| args                   | mean                                 |
+========================+======================================+
|  --threads             | the number of threads                |
+------------------------+--------------------------------------+
| --config               | tart port range                      | 
|                        | range(start_port, start_port+threads)|
+------------------------+--------------------------------------+
| --mode                 | ss or ssr (fake now)                 |
+------------------------+--------------------------------------+


