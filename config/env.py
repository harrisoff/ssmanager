# coding = utf-8

import sys

STATIC_PORTS = {
    '41111': 'password1',
    '42222': 'password2',
}

AUTH = 'password'

if 'win32' in sys.platform:
    # windows开发环境
    CONFIG_FILE = 'F:\Xshell Files\BAK\ss\shadowsocks.json.bak'
else:
    CONFIG_FILE = '/etc/shadowsocks.json'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your.ssserver.ip']