#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from remote import SendMsg
import json
import user


class QueryMsg(SendMsg):
    def __init__(self,username=None,mac=None,token=None,pid=None,vid="0000"):
        self.username=username
        self.mac=mac
        self.token=token
        self.pid=pid
        self.vid=vid

    def security_mode_query(self):
        return self.__send_msg("security_mode_change")

    def room_query(self):
        params={
            "room_id":-1
        }
        return self.__send_msg("room_manager",extend_params=params)

    def devices_query(self):
        params={
            "query_all":"yes",
        }
        return self.__send_msg("device_manager",extend_params=params)

    def combination_control_query(self):
        params={
            "comb_control_id":-1
        }
        return self.__send_msg("combination_control_manager",extend_params=params)

    def more_control_query(self):
        params={
            "m_c_name":"more_control_device"
        }
        return self.__send_msg("combination_control_manager",extend_params=params)

    def module_state_info_query(self):
        return self.__send_msg("module_state_info")

    def alarm_log_query(self,offset=0,count=15):
        params={
            "offset":offset,
            "count":count
        }
        return self.__send_msg("alarm_logs_info",extend_params=params)

    def alarm_pics_query(self,log_id=1):
        params={
            "log_id":log_id
        }
        return self.__send_msg("alarm_pics_info",extend_params=params)

    def __send_msg(self,msg_type,extend_params=None):
        cmd={
            "msg_type":msg_type,
            "command":"query",
            "from_role":"phone",
            "from_account":self.username
        }
        if extend_params:
            cmd.update(extend_params)
        sendmsg=self.__sendmsgformat(cmd)
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        print(res_msg)
        return res_msg


    def __sendmsgformat(self,msg=None):
        sendmsg={
            "cmd":"send_msg",
            "to_username":self.mac,
            "msg":json.dumps(msg),
            "subject":"control",
            "token":self.token
             }
        return sendmsg

    def get_dev_status(self):
        sendmsg={
            "cmd":"get_dev_status",
            "offset":"0",
            "total":"1048576",#1024*1024=1048576
            "pid":self.pid,
            "vid":self.vid,
            "to_username":self.mac,
            "token":self.token
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        if res_msg!="":
            self.OnDataCallback(res_msg)
        # print(res_msg)

    def get_code_to_register(self,phone):
        sendmsg={
            "cmd":"get_code_to_register",
            "phone":phone,
            "areacode":"86"
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

    def register_from_phone(self,phone,phonecode,pwd):
        sendmsg={
            "cmd":"register_from_phone",
            "from_username":phone,
            "phone_code":phonecode,
            "password":pwd,
            "type":"phone",
            "phone":phone
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

    def get_code_to_modify_password(self,phone):
        sendmsg={
            "cmd":"get_code_to_modify_password",
            "phone":phone,
            "areacode":"86"
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

    def reset_password(self,phone,phonecode,pwd):
        sendmsg={
            "cmd":"reset_password",
            "phone":phone,
            "phone_code":phonecode,
            "password":pwd
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

    def modify_password(self,pwd):
        sendmsg={
            "cmd":"modify_password",
            "new_password":pwd
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

    def get_all_friends(self):
        sendmsg={
            "cmd":"get_allfriend",
            "offset":"0",
            "total":"100",
            "token":self.token
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

    def get_unhandle_friend(self): #获取待处理的好友请求
        sendmsg={
            "cmd":"get_unhandle_friend",
            "offset":"0",
            "total":"100",
            "token":self.token
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        # if res_msg!="":
        #     self.OnDataCallback(res_msg)
        # print(res_msg)
        return res_msg

    def delete_friend(self): #删除好友
        sendmsg={
            "cmd":"del_friend",
            "to_username":self.mac,
            "token":self.token
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        # if res_msg!="":
        #     self.OnDataCallback(res_msg)
        # print(res_msg)
        return res_msg

    def add_friend(self,name,type): #添加好友
        sendmsg={
            "cmd":"add_friend",
            "to_username":self.mac,
            "token":self.token,
            "friend_name":name,
            "type":type,
            "addtype":type,
            "msg":""
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        # if res_msg!="":
        #     self.OnDataCallback(res_msg)
        # print(res_msg)
        return res_msg

    def OnDataCallback(self,msg):
        resmsg_dict=dict(eval(msg))
        if resmsg_dict.get("result",None)=="success":
            if resmsg_dict.get("usr",None):
                resmsg_usr_list=resmsg_dict.get("usr")
                user.set_data_dict("usr",resmsg_usr_list)
                # user.data_dict["usr"]=resmsg_usr_list
                # for l in resmsg_usr_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
            elif resmsg_dict.get("devlist",None):
                dev_list=resmsg_dict.get("devlist")
                rooms_list=dev_list[0]["rooms"]
                user.set_data_dict("rooms",rooms_list)
                # user.data_dict["rooms"]=rooms_list
                devices_list=dev_list[0]["devices"]
                user.set_data_dict("devices",devices_list)
                # user.data_dict["devices"]=devices_list
                combs_list=dev_list[0]["combs"]
                user.set_data_dict("combs",combs_list)
                # user.data_dict["combs"]=combs_list
                # for l in rooms_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
                # for l in devices_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
                # for l in combs_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))

