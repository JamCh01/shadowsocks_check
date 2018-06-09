#!/usr/bin/env python3
import os
import json
import queue
import psutil
import signal
import socket
import argparse
import requests
import subprocess
from threading import Thread

COMMOND = 'ss-local -s {server} -p {port} -l {local} -k {password} -m {method} {obfs}'
PROXIES = {
    'http': 'socks5h://127.0.0.1:{local}',
    'https': 'socks5h://127.0.0.1:{local}'
}
SOCKET_TIMEOUT = 2
MAX_COUNT = 8


def init_system():
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if 'ss-local' in p.name():
            for child in p.children():
                os.kill(child.pid, signal.SIGKILL)
            os.kill(p.pid, signal.SIGKILL)


def default_threads(path):
    return len(json.load(open(path)).get('configs'))


def get_config(path):
    configs = json.load(open(path)).get('configs')
    for config in configs:
        yield {
            'server': config.get('server'),
            'port': config.get('server_port'),
            'method': config.get('method'),
            'password': config.get('password'),
            'obfs': config.get('obfs'),
            'obfsparam': config.get('obfsparam')
        }


class QueueControl(object):
    def __init__(self):
        self.free = queue.Queue()

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
        self.obfs = self.kwargs.get('obfs')
        self.obfsparam = self.kwargs.get('obfsparam')
        if self.obfs == 'plain' and self.obfsparam == '':
            obfs = ''
        else:
            obfs = self.gen_obfs(obfs=self.obfs, obfsparam=self.obfsparam)
        commond = COMMOND.format(
            server=self.server,
            port=self.port,
            local=self.local,
            password=self.password,
            method=self.method,
            obfs=obfs)
        self.ss = subprocess.Popen(
            args=commond,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid)

    def gen_obfs(self, obfs, obfsparam):
        if obfs == 'simple_obfs_http':
            return '''--plugin obfs-local --plugin-opts "obfs={obfs_method};obfs-host={obfs_host}"'''.format(
                obfs_method='http', obfs_host=obfsparam)
        elif obfs == 'simple_obfs_tls':
            return '''--plugin obfs-local --plugin-opts "obfs={obfs_method};obfs-host={obfs_host}"'''.format(
                obfs_method='tls', obfs_host=obfsparam)

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
                url='https://api.ip.sb/jsonip',
                proxies=self.kwargs.get('proxies'),
                timeout=10)
            if r.json():
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

    def run(self):
        self.check()


def args_filter():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', dest='threads', type=int, default=0)
    parser.add_argument(
        '--start_port', dest='start_port', type=int, default=50000)
    parser.add_argument(
        '--config', dest='config_file', type=str, default='./gui-config.json')
    parser.add_argument('--mode', dest='mode', type=str, default='ss')
    args = parser.parse_args()
    return {
        'config_file':
        os.path.abspath(args.config_file),
        'threads_num':
        args.threads if args.threads else
        default_threads(path=os.path.abspath(args.config_file)),
        'start_port':
        args.start_port,
        'mode':
        args.mode
    }


def main():
    init_system()
    internal_config = args_filter()
    free_ports, configs = QueueControl(), QueueControl()
    for port in range(
            internal_config.get('start_port'),
            internal_config.get('start_port') +
            internal_config.get('threads_num')):
        free_ports.put(port)
    for config in get_config(path=internal_config.get('config_file')):
        configs.put(config)
    while not configs.is_empty():
        tasks = list()
        for i in range(internal_config.get('threads_num')):
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
