# -*- coding: utf-8 -*-

import os.path
import argparse

import ssh

hostname = 'stratos.ymotongpoo.com'
username = 'ymotongpoo'
password = 'rydeen83'
port = 20022
private_key_file = os.path.expanduser('~/.ssh/id_rsa')

client = ssh.SSHClient()
client.load_system_host_keys()
client.connect(hostname, username=username, password=password, port=port,
               key_filename=private_key_file)
print "**** exec python"
stdin, stdout, stderr = client.exec_command('sudo dmesg')
stdin.write('cimoon83')
stdin.flush()
print dir(stdin), type(stdin)
print ">>> stdin"
for l in stdout.read().split('\n'):
  print l

print ">>> stderr"
for l in stderr.read().split('\n'):
  print l

client.close()

