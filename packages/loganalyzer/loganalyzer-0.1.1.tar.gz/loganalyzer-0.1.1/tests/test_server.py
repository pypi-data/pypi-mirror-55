
import pytest
import logging
import threading
import time
import coloredlogs


def test_ssh_remote_host():
    import base64
    import paramiko

    host_key = b"""AAAAB3NzaC1yc2EAAAADAQABAAABAQDaQr4XN0Ar3A3VTSBR693r72S1GdsG1YCozpOEeewaQ/+c/lA+HbdlzHHv1EJ3VhFqOi44y+8FWGETYy9WAfDm9ti/oGBBKkl+/poF6qd2q0o0pqJOES+cVZeZswkLKDQbL9aa5o0amxVQeDMUbUtGXWU2U4oV5igT0U9yqHKdxKMtqUvGazMgaRPQFMJ1Hl3FrqOM4z9NOTTmby4AeXS9Vhz7+R48gpezDCtm3KQNCG3npgOBe4lDmNuByAtiTaUJc1o3Af+1QRZQl+kEj2cLnr3HC2lC+B3HuZL8Uad5hDxmeZNI0Qyr7Fof0I/TsLyXdXuvpzB8ge9o5ZUdIVvB"""

    client = paramiko.SSHClient()

    key = paramiko.RSAKey(data=base64.b64decode(host_key))
    client.get_host_keys().add('rp1', 'ssh-rsa', key)

    # conn = dict(hostname='rp1', username='agp', timeout=10)
    conn = dict(hostname='rp1', username='agp')
    client.connect(**conn)

    stdin, stdout, stderr = client.exec_command('ls -l')
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()

    foo = 1


def test_A():
    foo = 1

def test_B():
    pass

def test_C():
    pass

def test_D():
    pass

def test_E():
    pass

def test_F():
    pass

def test_G():
    pass

def test_H():
    pass

