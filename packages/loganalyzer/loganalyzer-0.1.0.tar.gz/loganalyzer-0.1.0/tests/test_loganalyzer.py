#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `loganalyzer` package."""

import pytest
import logging
import logging.config
import threading
import time
import yaml

import coloredlogs

from click.testing import CliRunner

from loganalyzer.loganalyzer import *
from loganalyzer import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'loganalyzer.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

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
    foo = 1

def test_2():
    config = 'logging.yaml'
    setup_config(config)
    # logging.basicConfig(level=logging.DEBUG)

    server = LoggerServer()

    log = logging.getLogger()
    log.warn('hello')
    time.sleep(1)

    logging.error('Hi from logging.yaml config file')
    time.sleep(1)

    server.stop()
    foo = 1

def test_3():
    conf = ConfigServer()
    client = LogClient()
    client.load_remote_config()

    assert client.config == server.config

    conf.stop()

    foo = 1

def test_4():
    pass

def test_5():
    pass

def test_6():
    pass

def test_7():
    pass

def test_8():
    pass

