#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import json
import requests
import time
import threading
import user
# from smarthome.share import queue
# from smarthome.share import logfile
from key import AESKey,RSAKey

POST_SECUREPORT_URL="http://server.atsmartlife.com/secureport"
POST_MSG_URL="http://server.atsmartlife.com/postmsg"
GET_URL="http://server.atsmartlife.com/getmsg"

AES_KEY="0000000000000000" #需要共享的变量
LOCK_KEY=threading.Lock() #锁

class PubPost(RSAKey):
    def request_post(self,msg):
        msg=json.dumps(msg)
        miwen=self._pub_encrypt(msg)
        res_msg=""
        try:
            response=requests.post(url=POST_SECUREPORT_URL,data=miwen,timeout=1)
            if response.status_code==200:
                res_msg=self._pub_decrypt(response.content)
        except requests.ConnectionError as e: #断开连接了
            print(e.message)
        except Exception as e:
            print(e.message)

        return res_msg

class SendMsg(AESKey):
    def _request(self,method,msg=None,params=None): #只有实例和子类使用
        global AES_KEY
        global LOCK_KEY
        res_msg=""
        response=""
        try:
            if method=="get":
                print("GET")
                try:
                    response=requests.get(url=GET_URL,params=params,timeout=65) #大多数请求外部服务器应该有一个超时,
                                                                              # 以防服务器没有响应及时。没有超时,那么您的代码就会挂几分钟或者更多
                except requests.ConnectionError as e: #get服务断开连接，每60秒请求一次
                    time.sleep(60)

                except requests.ConnectTimeout as e:
                    print("get Timeout error")
                except Exception as e:
                    print(e.message)
            else :
                print("POST")
                jsonmsg=json.dumps(msg)
                print(jsonmsg)
                if LOCK_KEY.acquire():
                    miwen=self._aes_encrypt(AES_KEY,jsonmsg)
                    LOCK_KEY.release()
                    try:
                        response=requests.post(url=POST_MSG_URL,data=miwen,timeout=2)
                    except Exception as e:
                        print(e.message)
            if response!="":
                if response.status_code==200:
                    if LOCK_KEY.acquire():
                        try:
                            res_msg=self._aes_decrypt(AES_KEY,response.content)
                            LOCK_KEY.release()
                        except Exception as e:
                            print("aes_decrypt",e.message)
                            LOCK_KEY.release()#避免死锁
                            exptime=GetAesKey().get_aes()

        except Exception as e:
            print(e.message)

        finally:
            return res_msg

class LoginManage(PubPost):
    def __init__(self,username,password):
        self.username=username
        self.password=password

    def login(self):
        #登录，获取token--调通
        try:
            msg={"cmd":"login","from_username":self.username,"password":self.password}
            res_msg=self.request_post(msg)
            if res_msg!="":
                res_msg2=dict(res_msg)
                if res_msg2.get("result",None)=="success":
                    print("Login success")
                    token=res_msg2.get("token")
                    return token
                else:
                    return ""
            else:
                return ""
        except Exception as e:
            print(e.message)

    # def loginout(self):
    #     #退出登录
    #     sendmsg={"cmd":"logout"}
    #     res_msg=self._request("post",msg=sendmsg)
    #     return res_msg

class GetAesKey(PubPost):
    def get_aes(self):
        #获取动态aes密码--调通
        global AES_KEY
        global LOCK_KEY
        expiretime=0
        try:
            timenow=str(int(time.time()))
            msg={"cmd":"get_dynamic_passwd","time":timenow}
            res_msg=self.request_post(msg)
            if res_msg!="":
                res_msg2=dict(res_msg)
                if LOCK_KEY.acquire():
                    AES_KEY=res_msg2.get("dynamic_passwd","0000000000000000")
                    user.set_info_dict("AESKEY",AES_KEY)
                    print("AESKEY change:",AES_KEY)
                    temp_key="AesKeyChange==="+AES_KEY
                    print(temp_key)
                    LOCK_KEY.release()
                    expiretime=int(res_msg2.get("expire",0))
        except Exception as e:
            print(e.message)
        finally:
            return int(expiretime/1000)
