#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import threading
#pid:设备号，舒睡宝是“0001”室内机0002,协调器“0003”
#空气盒子0004, WIFI门锁0005,服务型机器人0006，扫地机0007,魔镜：0008，无屏主机0009

info_dict={}     #基本信息：AESKEY
info_lock=threading.RLock()
def get_info_dict(key):
    global info_dict
    global info_lock
    info=""
    if info_lock.acquire():
        info=info_dict.get(key,None)
        info_lock.release()
    return info

def set_info_dict(key,value):
    global info_dict
    global info_lock
    if info_lock.acquire():
        info_dict[key]=value
        info_lock.release()

