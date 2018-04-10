#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
import json
from utils import business,user,query,control
import time
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from smarthome.forms import SmartHomeUserForm
from smarthome.models import *
import hashlib

# Create your views here.
def smarthome_login(request):
    errors=[]
    if request.is_ajax():
        print("come in ajax")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        aeskey=""
        result=""
        token=business.login(str(username),str(password))
        time.sleep(1)
        print(token)
        if token:
            try:
                smarthome_user=SmartHomeUser.objects.get(username=username)
            except SmartHomeUser.DoesNotExist:
                smarthome_user=SmartHomeUser()
            smarthome_user.username=username
            smarthome_user.password=password
            smarthome_user.token=token
            smarthome_user.save()
            aeskey=user.get_info_dict("AESKEY")
            # aeskey="6x5v321oso76ruvr"
            print(aeskey)
            result=query.QueryMsg(token=token).get_all_friends()
            print(result)
        else:
            errors.append(u"用户名或者密码错误!")

        mydict = {"token":token,"aeskey":aeskey,"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
    else:
        return render(request,"smarthome-login.html","")


# def smarthome_control(request):

def md5(pwd):
    """
    九宫格排列：
    0 1 2
    3 4 5
    6 7 8
    :param str:
    :return:
    """
    new_pwd=""
    for i in range(len(pwd)):
        new_pwd+=str(int(pwd[i])-1)
    print(new_pwd)
    m = hashlib.md5()
    m.update(new_pwd)
    return m.hexdigest()


class UpdateInfo(View):
    def post(self, request, *args, **kwargs):
        #获取要对用户进行什么操作
        slug = self.kwargs.get('slug')
        if slug == 'aeskey':
            return self.updata_aeskey(request)
        elif slug == "token":
            return self.updata_token(request)
        elif slug=='getfriends':
            return self.get_all_friends(request)
        elif slug=='getall':
            return self.get_all_query(request)
        elif slug=='scene':
            return self.control_scene(request)
        elif slug=='light':
            return self.control_light(request)
        elif slug=='curtain':
            return self.control_curtain(request)
        elif slug=='safety':
            return self.control_safety(request)
        elif slug=="logout":
            return self.user_logout(request)
        elif slug=="getunhandlefriend":
            return self.get_unhandle_friend(request)
        elif slug=="delfriend":
            return  self.del_friend(request)
        elif slug=="addfriend":
            return  self.add_friend(request)
        elif slug=="getcode":
            return self.get_register_code(request)
        elif slug=="register":
            return self.register(request)
        elif slug=="getcodemodify":
            return self.get_modify_code(request)
        elif slug=="resetpwd":
            return self.reset_password(request)
        else:
            raise PermissionDenied

    def get_modify_code(self,request):
        phone=str(request.POST.get("phone", ""))
        errors=[]
        result=query.QueryMsg().get_code_to_modify_password(phone)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def reset_password(self,request):
        phone=str(request.POST.get("phone", ""))
        phonecode=str(request.POST.get("phonecode", ""))
        password=str(request.POST.get("password", ""))
        errors=[]
        result=query.QueryMsg().reset_password(phone,phonecode,password)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def get_register_code(self,request):
        phone=str(request.POST.get("phone", ""))
        errors=[]
        result=query.QueryMsg().get_code_to_register(phone)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def register(self,request):
        phone=str(request.POST.get("phone", ""))
        phonecode=str(request.POST.get("phonecode", ""))
        password=str(request.POST.get("password", ""))
        errors=[]
        result=query.QueryMsg().register_from_phone(phone,phonecode,password)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def updata_aeskey(self,request):
        aeskey=user.get_info_dict("AESKEY")
        mydict = {"aeskey": aeskey}
        print(aeskey)
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def updata_token(self,request):
        username = request.POST.get("username", "")
        to_user=SmartHomeUser.objects.get(username=str(username))
        password=to_user.password
        token=business.login(str(username),str(password))
        errors=[]
        if token:
            to_user.token=token
            to_user.save()
        else:
            errors.append(u"登录失败！")

        mydict={"errors":errors,"token":token}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def user_logout(self,request):
        token=str(request.POST.get("token", ""))
        errors=[]
        print("logout-post-token",token)
        result=business.logout(token)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )


    def get_all_friends(self,request):
        token=str(request.POST.get("token", ""))
        errors=[]
        result=query.QueryMsg(token=token).get_all_friends()
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def del_friend(self,request):
        token=str(request.POST.get("token", ""))
        mac=str(request.POST.get("mac", ""))
        errors=[]
        result=query.QueryMsg(token=token,mac=mac).delete_friend()
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def add_friend(self,request):
        token=str(request.POST.get("token", ""))
        mac=str(request.POST.get("mac", ""))
        friend_name=str(request.POST.get("friend_name", ""))
        typename=str(request.POST.get("type", ""))
        errors=[]
        result=query.QueryMsg(token=token,mac=mac).add_friend(friend_name,typename)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def get_unhandle_friend(self,request):
        token=str(request.POST.get("token", ""))
        errors=[]
        result=query.QueryMsg(token=token).get_unhandle_friend()
        print("get_unhandle_friend-post:",result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def get_all_query(self,request):
        token=str(request.POST.get("token", ""))
        from_username=str(request.POST.get("from_username", ""))
        username=str(request.POST.get("username", ""))
        errors=[]
        result=[]
        Q=query.QueryMsg(token=token,mac=from_username,username=username)

        res=Q.security_mode_query()
        result.append(res)

        res=Q.room_query()
        result.append(res)

        res=Q.combination_control_query()
        result.append(res)

        res=Q.devices_query()
        result.append(res)
        print(result)
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def control_scene(self,request):
        token=str(request.POST.get("token", ""))
        from_username=str(request.POST.get("from_username", ""))
        username=str(request.POST.get("username", ""))
        control_name=request.POST.get("control_name", "")#unicode
        # print(type(control_name))
        control_name=control_name.encode('utf-8')#utf-8
        # print(type(control_name))
        result=control.Control(token=token,username=username,mac=from_username).scene_c(control_name)
        errors=[]
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def control_light(self,request):
        token=str(request.POST.get("token", ""))
        from_username=str(request.POST.get("from_username", ""))
        username=str(request.POST.get("username", ""))
        room_name=request.POST.get("room_name", "").encode('utf-8')#unicode---utf-8
        dev_name=request.POST.get("dev_name", "").encode('utf-8')#unicode---uf-8
        func_command=request.POST.get("fun_command", "")#
        print(room_name)
        result=control.Control(token=token,username=username,mac=from_username).light_c(room_name,dev_name,func_command)
        print(result)
        errors=[]
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def control_curtain(self,request):
        token=str(request.POST.get("token", ""))
        from_username=str(request.POST.get("from_username", ""))
        username=str(request.POST.get("username", ""))
        room_name=request.POST.get("room_name", "").encode('utf-8')#unicode---utf-8
        dev_name=request.POST.get("dev_name", "").encode('utf-8')#unicode---uf-8
        func_command=request.POST.get("fun_command", "")#
        print(room_name)
        result=control.Control(token=token,username=username,mac=from_username).curtain_c(room_name,dev_name,func_command)
        print(result)
        errors=[]
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )

    def control_safety(self,request):
        token=str(request.POST.get("token", ""))
        from_username=str(request.POST.get("from_username", ""))
        username=str(request.POST.get("username", ""))
        security_mode=str(request.POST.get("security_mode", ""))
        password=str(request.POST.get("password", ""))
        print("disarm_password:",password)
        password=md5(password)
        print("enc_disarm_password:",password)
        result=control.Control(token=token,username=username,mac=from_username).security_mode_c(security_mode,password=password)
        print("post_return:",result)
        errors=[]
        mydict={"errors":errors,"result":result}
        return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )