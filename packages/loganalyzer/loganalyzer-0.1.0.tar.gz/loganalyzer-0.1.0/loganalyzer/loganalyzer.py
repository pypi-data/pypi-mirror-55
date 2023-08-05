# -*- coding: utf-8 -*-

"""Main module."""

import logging
import logging.config
import threading
import time
import os
import re
import random
import socket
import select
import yaml
import ujson as json
import zlib
import pickle
from utools.ulogging import setup_config

import socket

class LogAgent(object):
    DEFAULT_ADDRESS = ('', 9999)
    QUERY = b'GET /config'

    def __init__(self):
        self.config = dict()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def load_config(self, pattern):
        if pattern:
            self.config = setup_config(pattern)


class LogServer(LogAgent):

    def __init__(self, config_file=None, address=None):
        super(LogServer, self).__init__()

        self.config_file = config_file or self.DEFAULT_CONFIG
        self.address = address or self.DEFAULT_ADDRESS
        self.load_config(self.config_file)
        self.running = False
        self.th = None
        self.serve(self.address)

    def serve(self, address):
        if address:
            self.sock.bind(address)
            self.address = address
            self.th = threading.Thread(target=self._run)
            self.th.start()

    def stop(self):
        self.running = False
        self.th.join(timeout=5)

    def _run(self):
        self.running = True
        while self.running:
            r, _, _ = select.select([self.sock], [], [], 1)
            if r:
                data, address = self.sock.recvfrom(0x4000)
                self._handle(data, address)

    def _handle(self, data, address):
        raise RuntimeError("Must be overriden")

class ConfigServer(LogServer):
    "Server log config using UDP"
    DEFAULT_ADDRESS = ('', 9998)
    DEFAULT_CONFIG = 'logging.yaml'

    def _handle(self, data, address):
        if data == self.QUERY:
            data = bytes(json.encode(self.config), encoding='utf-8')
            data = zlib.compress(data)
            self.sock.sendto(data, address)

class LoggerServer(LogServer):
    "Dump records received by UDP using local handlers (config file)"
    DEFAULT_CONFIG = 'server.yaml'

    def _handle(self, data, address):
        data = pickle.loads(data[4:])
        record = logging.makeLogRecord(data)
        logging.root.handle(record)
        foo = 1


class LogClient(LogAgent):
    def __init__(self, address=None):
        super(LogClient, self).__init__()
        self.address = address or ('', random.randint(1024, 64000))
        self.sock.bind(self.address)

    def load_remote_config(self, address=None):
        address = address or self.DEFAULT_ADDRESS
        data = self.QUERY
        for tries in range(10):
            self.sock.sendto(data, address)
            r, _, _ = select.select([self.sock], [], [], 1)
            if r:
                data, addr = self.sock.recvfrom(0x4000)
                data = zlib.decompress(data)
                self.config = json.decode(data)
                logging.config.dictConfig(self.config)
                break


def test_1():
    def worker(arg):
        while not arg['stop']:
            logging.debug('Hi from myfunc')
            time.sleep(0.5)

    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    info = {'stop': False}

    coloredlogs.install(level=logging.DEBUG)

    thread = threading.Thread(target=worker, args=(info,))
    thread.start()
    for i in range(10):
        logging.debug('Hello from main')
        time.sleep(0.75)

    info['stop'] = True
    thread.join()

def test_2():
    config = 'logging.yaml'
    setup_config(config)

    logging.debug('Hi from logging.yaml config file')

    foo = 1

if __name__ == '__main__':
    # test_1()
    test_2()

    foo = 1
