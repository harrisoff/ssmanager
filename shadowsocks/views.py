# coding = utf-8

import json

from django.shortcuts import render
from django.shortcuts import HttpResponse

from shadowsocks.utils import if_running, ss_start, list_ports, add_port, del_port


def status(request):
    running, msg = if_running()
    running = 'y' if running else 'n'
    resp = json.dumps({'errcode': 0, 'status': running, 'msg': msg})
    return HttpResponse(resp, content_type="application/json")


def start(request):
    started, msg = ss_start()
    started = 'y' if started else 'n'
    resp = json.dumps({'errcode': 0, 'status': started, 'msg': msg})
    return HttpResponse(resp, content_type="application/json")


def add(request, port, pswd, auth):
    status, msg = add_port(port, pswd, auth)
    status = 'y' if status else 'n'
    resp = json.dumps({'errcode': 0, 'status': status, 'msg': msg})
    return HttpResponse(resp, content_type="application/json")


def delete(request, port, auth):
    status, msg = del_port(port, auth)
    status = 'y' if status else 'n'
    resp = json.dumps({'errcode': 0, 'status': status, 'msg': msg})
    return HttpResponse(resp, content_type="application/json")


def lists(request):
    port_password = list_ports()
    resp = json.dumps({'errcode': 0, 'data': port_password})
    return HttpResponse(resp, content_type="application/json")


def page(request):
    return render(request, 'shadowsocks.html')
