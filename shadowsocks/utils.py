# coding = utf-8

import os, json, re

from config.env import STATIC_PORTS, AUTH, CONFIG_FILE


# 重启ss
def ss_restart():
    cmd('ssserver -c %s -d restart' % CONFIG_FILE)
    if if_running():
        return True, '启动成功'
    return False, '启动失败，重试或联系管理员'


# 启动ss
def ss_start():
    cmd('ssserver -c %s -d start' % CONFIG_FILE)
    if if_running():
        return True, '启动成功'
    return False, '启动失败，重试或联系管理员'


# 停止ss
def ss_stop():
    cmd('ssserver -c %s -d stop' % CONFIG_FILE)
    if if_running():
        return False
    return True


# 执行命令
def cmd(command):
    stdout = os.popen(command).read()
    return stdout


# 过滤不显示的端口
def filter_ports(conf_dic):
    for port in STATIC_PORTS:
        if port in conf_dic:
            conf_dic.pop(port)
    return conf_dic


def auth_check(auth):
    return auth == AUTH


# 读取配置文件
def read_conf():
    with open(CONFIG_FILE) as f:
        content = json.loads(f.read())
        return content


# 写入配置文件 - 接受一个完整的port_password参数，这里只负责写入
def write_conf(port_password):
    with open(CONFIG_FILE, 'r+') as f:
        # 读取配置文件
        conf = json.loads(f.read())
        # 删除现有port_password
        conf.pop('port_password')
        # 替换为新的port_password
        conf['port_password'] = port_password
        # 移动指针至开头
        f.seek(0)
        # 写入
        f.write(json.dumps(conf))
        f.truncate()
        return True


# 是否运行
def if_running():
    stdout = cmd('ps -aux | grep ssserver')
    reg = re.compile('ssserver -c /etc/')
    running = re.search(reg, stdout)
    if running:
        return True, '运行正常'
    return False, '服务已停止'


# 添加端口
def add_port(port, pswd, auth):
    # 格式化
    port = str(port)
    # 验证密码
    if not auth_check(auth):
        return False, '添加失败，授权码错误'
    # 验证端口是否已经存在
    port_password = list_all_ports()
    if port in port_password:
        return False, '添加失败，该端口已在使用'
    # 添加
    port_password[port] = pswd
    # 写回
    write_conf(port_password)
    # 重启
    restarted, msg = ss_restart()
    if restarted:
        return True, '添加成功'
    return False, '添加成功，重启失败'


# 删除端口
def del_port(port, auth):
    # 验证密码
    if not auth_check(auth):
        return False, '删除失败，授权码错误'
    # 验证该端口是否可操作
    if port in STATIC_PORTS:
        return False, '删除失败，没有操作权限'
    # 读
    port_password = list_all_ports()
    # 验证端口是否存在
    if not port in port_password:
        return False, '删除失败，端口不存在'
    # 删
    port_password.pop(port)
    # 写回
    write_conf(port_password)
    # 重启
    restarted, msg = ss_restart()
    if restarted:
        return True, '删除成功'
    return False, '删除成功，重启失败'


# 列出有权限查看的端口和密码
def list_ports():
    return filter_ports(read_conf()['port_password'])


# 列出所有端口和密码
def list_all_ports():
    return read_conf()['port_password']