#!/usr/bin/env python3
import os
# import ping
import json
import queue
import psutil
import signal
import socket
import requests
import subprocess
from time import sleep
from threading import Thread

COMMOND = 'ss-local -s {server} -p {port} -l {local} -k {password} -m {method} -t 2'
SS_CONFIG = './gui-config.json'
PROXIES = {
    'http': 'socks5h://127.0.0.1:{local}',
    'https': 'socks5h://127.0.0.1:{local}'
}
SOCKET_TIMEOUT = 2
MAX_COUNT = 8
PORT_RANGE = range(50000, 50010)
GETPORTCOUNT = 4


def init():
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if 'ss-local' in p.name():
            for child in p.children():
                os.kill(child.pid, signal.SIGKILL)
            os.kill(p.pid, signal.SIGKILL)


def json_filter(path):
    configs = json.load(open(path)).get('configs')
    for config in configs:
        yield {
            'server': config.get('server'),
            'port': config.get('server_port'),
            'method': config.get('method'),
            'password': config.get('password'),
        }


class QueueControl(object):
    def __init__(self):
        self.free = queue.Queue()

    def init_queue(self):
        for i in PORT_RANGE:
            self.free.put(i)

    def put(self, i):
        self.free.put(i)

    def get(self):
        return self.free.get(timeout=5)

    def is_empty(self):
        return self.free.empty()

    @property
    def size_of(self):
        return self.free.qsize()


class Shadowsocks(Thread):
    def __init__(self, kwargs):
        Thread.__init__(self)
        self.kwargs = kwargs
        self.server = self.kwargs.get('server')
        self.port = self.kwargs.get('port')
        self.local = self.kwargs.get('local')
        self.password = self.kwargs.get('password')
        self.method = self.kwargs.get('method')
        commond = COMMOND.format(
            server=self.server,
            port=self.port,
            local=self.local,
            password=self.password,
            method=self.method)
        self.ss = subprocess.Popen(
            args=commond,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid)

    def tcping(self, host, port):
        count, pass_count, fail_count = 0, 0, 0
        while count < MAX_COUNT:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            no_error = False
            s.settimeout(SOCKET_TIMEOUT)
            try:
                s.connect((host, int(port)))
                s.shutdown(socket.SHUT_RD)
                no_error = True
            except Exception as e:
                fail_count += 1
                count += 1
                continue

            if no_error:
                pass_count += 1
            count += 1
        if fail_count > 4:
            return False
        else:
            return True

    def check(self):
        try:
            r = requests.get(
                url='https://www.google.com',
                proxies=self.kwargs.get('proxies'),
                timeout=10)
            if '<title>Google</title>' not in r.text:
                if self.tcping(host=self.server, port=self.port):
                    print('{server} 检测正常'.format(server=self.server))
                else:
                    print('{server} 疑似存在问题，请核查'.format(self.server))
            else:
                print('{server} 检测正常'.format(server=self.server))

        except Exception as e:
            if self.tcping(host=self.server, port=self.port):
                print('{server} 检测正常'.format(server=self.server))
            else:
                print('{server} 确认存在问题，请核查'.format(server=self.server))
        os.killpg(os.getpgid(self.ss.pid), signal.SIGTERM)
        self.kwargs.get('queue').put(self.local)
        sleep(5)

    def run(self):
        self.check()


def main():
    init()
    free_ports = QueueControl()
    free_ports.init_queue()
    configs = QueueControl()
    for config in json_filter(path=SS_CONFIG):
        configs.put(config)
    while not configs.is_empty():
        tasks = list()
        for i in range(len(PORT_RANGE)):
            try:
                config = configs.get()
                local = free_ports.get()
                proxies = PROXIES.copy()
                proxies['http'] = proxies['http'].format(local=local)
                proxies['https'] = proxies['https'].format(local=local)
                config.setdefault('local', local)
                config.setdefault('proxies', proxies)
                config.setdefault('queue', free_ports)
                task = Shadowsocks(kwargs=config)
                tasks.append(task)
            except queue.Empty:
                pass

        for task in tasks:
            task.start()
        for task in tasks:
            task.join()


if __name__ == '__main__':
    main()