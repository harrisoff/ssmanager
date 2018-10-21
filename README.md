# shadowsocks管理页面

[TOC]

## 简介

django开发的shadowsocks管理页面。适配移动端。

适用于**python版本的shadowsocks服务端**。

打开网页就可以管理shadowsocks，免去了登服务器输命令的麻烦。

依赖：
- `python3.x`
- `django2.0.x`

功能：
- 查看运行状态
- 启动服务
- 添加端口并重启
- 删除端口并重启

提示：

添加端口和删除端口功能**可能**有问题。

因为修改配置文件后需要重启，而最近发现有时`ssserver -c /etc/ss.json -d stop`不能正常停止服务。

导致虽然配置文件修改成功，但是重启失败，所以修改并没有生效。

警告：

需要以root权限运行，否则不能操作shadowsocks的pid文件，也就不能实现重启。

所以有安全风险。~~其实一开始根本没考虑什么安全问题。~~

## 使用

部署后访问`http://ip:port/ss/admin`

共3个标签页：

- 状态页

  显示运行状态。未运行时，启动ss服务。
  
- 添加端口页

  添加端口和密码到ss配置文件，自动重启ss服务。
  
- 删除端口页

  从ss配置文件删除端口，自动重启ss服务。

### 状态页
未运行时点击启动ss服务。

![运行正常](https://raw.githubusercontent.com/harrisoff/images-host/master/ssmanager/ssmanager1-status-running-small.png) ![未运行](https://raw.githubusercontent.com/harrisoff/images-host/master/ssmanager/ssmanager2-status-stopped-small.png)

### 添加端口页
授权码其实就是密码，（象征性地）起验证作用。

添加成功或失败有相应提示。

![添加端口页](https://raw.githubusercontent.com/harrisoff/images-host/master/ssmanager/ssmanager3-add-small.png)

### 删除端口页
显示目前配置文件中的端口和密码，点击删除。

可以设置不显示某些端口。

![删除端口页](https://raw.githubusercontent.com/harrisoff/images-host/master/ssmanager/ssmanager4-del-small.png)

## 配置和部署

### 配置

都在`/config/env.py`文件中。

- `STATIC_PORTS`

  不希望显示到删除页面的端口。

- `AUTH`

  授权码。

- `CONFIG_FILE`

  shadowsocks配置文件路径。默认为`/etc/shadowsocks.json`。

- `ALLOWED_HOSTS`

 即`settings.py`里的`ALLOWED_HOSTS`。为了修改方便，放到这里。

### 部署

略。

## 其他

### shadowsocks.json格式

对象或数组的最后一项之后不要加逗号，否则`json.loads()`会抛异常。
```
# 错误
"port_password": {
  "41111": "myphonepswd",
  "41112": "raspberrypi",
}
# 正确
"port_password": {
  "41111": "myphonepswd",
  "41112": "raspberrypi"
}
```

### 数据校验

没有很严格的数据校验，比如后端没有再次判断输入的端口是否为整数。

默认输入基本都是合法的。（毕竟谁会跟自己用的工具过不去
