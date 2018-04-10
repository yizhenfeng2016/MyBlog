#coding:utf-8
__author__ = 'Administrator'

from remote import LoginManage,GetAesKey,SendMsg
import user
# from smarthome.query.query import QueryMsg
# from smarthome.msgmanage import getservice
import socket
from threading import Thread
import time

HostName="server.atsmartlife.com"

def login(username,password):
    token=""
    if len(password)>=6 and len(password)<=16:
        token=LoginManage(username,password).login()
        print(token)
    return token

def logout(token):
    cmd={
        "cmd":"logout",
        "token":token
    }
    res=SendMsg()._request("post",msg=cmd)
    return res

class getAesKeyThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.GetAesKey=GetAesKey()
        self.running=True
        self.flag=True

    def run(self):
        # print("start getAesKeyThread")
        timer_interval=self.GetAesKey.get_aes()
        print(timer_interval)
        while self.running:
            time.sleep(timer_interval)
            if self.flag:
                timer_interval=self.GetAesKey.get_aes()
                print(timer_interval)

    def pause(self):
        self.flag=False

    def resume(self):
        self.flag=True

    def stop(self):
        self.flag=True # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running=False



# if __name__=="__main__":
#     key_thread_p=getAesKeyThread()
#     key_thread_p.start() #动态获取密钥线程
    # token=login("13600000003","123456")
    # print("token",token)
#     time.sleep(1)
#     print("aeskey",user.get_info_dict("AESKEY"))
#     while True:
#         get_msg()