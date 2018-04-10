/**
 * Created by Administrator on 2018/1/22.
 */

var getMsgUtil=(function(callback){

    var obj = new Object();
    obj.aesKey =  window.localStorage["debug"];
    obj.count = 0;
    obj.baseurl='http://'+window.location.host+'/static/';

    /**
     *
     * @param {type} data BASE64的数据
     * @param {type} key 解密秘钥
     * @param {type} iv 向量
     * @returns {undefined}
     */
     obj.aesDecrypt = function(data, keyStr) {
        var key = CryptoJS.enc.Utf8.parse(keyStr);
        //解密的是基于BASE64的数据，此处data是BASE64数据
        var decrypted = CryptoJS.AES.decrypt(data, key, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.ZeroPadding});
        return decrypted.toString(CryptoJS.enc.Utf8);
    };

    /**
     * 加密数据
     * @param {type} data 待加密的字符串
     * @param {type} keyStr 秘钥
     * @param {type} ivStr 向量
     * @returns {unresolved} 加密后的数据
     */
     obj.aesEncrypt = function(data, keyStr) {
        var sendData = CryptoJS.enc.Utf8.parse(data);
        var key = CryptoJS.enc.Utf8.parse(keyStr);
        var encrypted = CryptoJS.AES.encrypt(sendData, key,{mode:CryptoJS.mode.ECB,padding:CryptoJS.pad.ZeroPadding});
        return CryptoJS.enc.Base64.stringify(encrypted.ciphertext);
    };


    obj.updateTokenTime = function(phone){
        console.log("updataTokenTime");
        $.ajax({
                url : 'http://'+window.location.host+'/smarthome/update/token',
                type : "POST",
                dataType:'json',
                data : {
                    "username":phone
                },
                success : function(data){
                    obj.count=0;
                    console.log(data);
                    var errors = data["errors"];
                    if(errors.length==0){
                        window.localStorage["text"]=data["token"];
                    }
                    else{
                        alert(errors);
                    }
                },
                error : function(error){
                    console.log(error);
                }
            });
    };
    obj.updateAeskey=function(){
        $.ajax({
                url : 'http://'+window.location.host+'/smarthome/update/aeskey',
                type : "POST",
                dataType:'json',
                success : function(data){
                    console.log(data);
                    window.localStorage["debug"]=data["aeskey"];
                    console.log("aeskey:"+window.localStorage["debug"]);
                },
                error : function(error){
                    console.log(error);
                }
            });
    }

    obj.message = function(result){
            var data  = {};
            data.from_username=result.from_username;
            data.data=result.msg.data;
            console.log("message");
            //var url ='http://'+window.location.host+'/smarthome/index.php/Main/message';
            //
            //$.ajaxUtil(url, 'post',{data:data}, function (data) {
            //    console.log(data);
            //}, function (error) {
            //    console.log(error)
            //});
    }

    obj.light=function(data){
        var id = data.room_name+","+data.device_name;
        //  alert(id);
        if(data.dev_state==undefined) {
            return;
        }
        console.log(data.dev_state);
        if(data.dev_state.power==="on"){
            console.log("light on");
            $("div[deviceid='"+id+"']").find('a').removeClass().addClass('switch_on');
            $("div[deviceid='"+id+"']").find('.light_state').text('已开启');
            $("div[deviceid='"+id+"']").find('.img_light_state').find("img").attr("src",obj.baseurl+'blog/img/smarthome/shebei_light_on.png');


        }
        if(data.dev_state.power==="off"){
            console.log("light off");
            $("div[deviceid='"+id+"']").find('a').removeClass().addClass('switch_off');
            $("div[deviceid='"+id+"']").find('.light_state').text('已关闭');
            $("div[deviceid='"+id+"']").find('.img_light_state').find("img").attr("src",obj.baseurl+'blog/img/smarthome/shebei_light_off.png');

        }

    }

    obj.curtain=function(data){
        var id = data.room_name+","+data.device_name;
        if(data.dev_state==undefined) {
            return;
        }
        if(data.dev_state.power==="open"){
            $("div[deviceid='"+id+"']").find('.curtain_state').text('开窗');
            var d=$("div[deviceid='"+id+"']").find('a');
            $(d[0]).removeClass("curtain_open_n").addClass("curtain_open_c");
            $(d[1]).removeClass("curtain_stop_c").addClass("curtain_stop_n");
            $(d[2]).removeClass("curtain_close_c").addClass("curtain_close_n");

        }

        if(data.dev_state.power==="stop"){
             $("div[deviceid='"+id+"']").find('.curtain_state').text('暂停');
             var d=$("div[deviceid='"+id+"']").find('a');
             $(d[0]).removeClass("curtain_open_c").addClass("curtain_open_n");
             $(d[1]).removeClass("curtain_stop_n").addClass("curtain_stop_c");
             $(d[2]).removeClass("curtain_close_c").addClass("curtain_close_n");

        }

        if(data.dev_state.power==="close"){
             $("div[deviceid='"+id+"']").find('.curtain_state').text('关窗');
             var d=$("div[deviceid='"+id+"']").find('a');
             $(d[0]).removeClass("curtain_open_c").addClass("curtain_open_n");
             $(d[1]).removeClass("curtain_stop_c").addClass("curtain_stop_n");
             $(d[2]).removeClass("curtain_close_n").addClass("curtain_close_c");

        }
    }

    obj.sceneCanvasDraw=function(canvas_obj,t){
        //alert("点击");
			var canvas=canvas_obj,
			//var canvas = document.getElementById('canvas'),  //获取canvas元素
				context = canvas.getContext('2d'),  //获取画图环境，指明为2d
				centerX = canvas.width/2,   //Canvas中心点x轴坐标
				centerY = canvas.height/2,  //Canvas中心点y轴坐标
				rad = Math.PI*2/100, //将360度分成100份，那么每一份就是rad度
				speed = 0, //加载的快慢就靠它了
				time_s=1.8/t; //决定运行时间
            var gradient=context.createLinearGradient(0,0,170,0);
			gradient.addColorStop("0","magenta");
			gradient.addColorStop("0.5","blue");
			gradient.addColorStop("0.8","red");

            var imgobj=new Image();
            imgobj.src=obj.baseurl+'blog/img/smarthome/scene_success.png';

			//绘制5像素宽的运动外圈
			function blueCircle(n){
				context.save();
				context.strokeStyle = gradient; //设置描边样式
				context.lineWidth = 5; //设置线宽
				context.beginPath(); //路径开始
				context.arc(centerX, centerY, 35 , -Math.PI/2, -Math.PI/2 +n*rad, false); //用于绘制圆弧context.arc(x坐标，y坐标，半径，起始角度，终止角度，顺时针/逆时针)
				context.stroke(); //绘制
				context.closePath(); //路径结束
				context.restore();
			}
			//绘制白色外圈
			function whiteCircle(){
				context.save();
				context.beginPath();
				context.lineWidth = 5; //设置线宽
				context.strokeStyle = "gray";
				context.arc(centerX, centerY, 35 , 0, Math.PI*2, false);
				context.stroke();
				context.closePath();
				context.restore();
			}
			//动画循环
			(function drawFrame(){
				if(speed<=100){
					window.requestAnimationFrame(drawFrame);
					context.clearRect(0, 0, canvas.width, canvas.height);
					whiteCircle();
					//text(speed);
					blueCircle(speed);
					speed+=time_s;
				}
				else{
				    context.clearRect(0, 0, canvas.width, canvas.height);
					//alert("执行成功");
                    context.drawImage(imgobj,0,0,80,80);
                    setTimeout(function(){ context.clearRect(0, 0, canvas.width, canvas.height);}, 1000);//延时1秒
				}

			}());
    };
    obj.filterMessage = function (data){
        var result =  JSON.parse(data);
        if(result.cmd=='add_friend'){
            window.localStorage.user_badger=1;
            if(result.type==='gateway'){
                //$.ajax({
                //    url : 'http://'+window.location.host+'/smarthome/index.php/Main/addsubscript',
                //    type : "POST",
                //    dataType : "text",
                //    data : {
                //        type: "friend"
                //    },
                //    success : function(data){
                //        $.console.log(data);
                //    },
                //    error : function(error){
                //        $.console.log(error);
                //    }
                //});
                //
                //var imgUrl = getRootPath()+"/application/views/plugin/app/images/icon_snj_02.png";
                //var content ='<div class="bangd_main_img"><img src='+imgUrl+'></div>';
                //$.bindDialog('有室内机请求绑定',content,'忽略','同意绑定',function(){
                //    $('#myroom_item').find('.myroom_info').remove();
                //    $('#myroom_item').append('<em class="myroom_info" ></em>');
                //    $.closeDialog();
                //},function(){
                //    window.location.href='http://'+window.location.host+'/smarthome/index.php/Main/myroom';
                //});
                console.log("add_friend");
            }

            if(result.type==='village'){
                //$.ajax({
                //    url : 'http://'+window.location.host+'/smarthome/index.php/Main/addsubscript',
                //    type : "POST",
                //    dataType : "text",
                //    data : {
                //        type: "village"
                //    },
                //    success : function(data){
                //        $.console.log(data);
                //    },
                //    error : function(error){
                //        $.console.log(error);
                //    }
                //});
                console.log("village");
            }

        }

        if(result.cmd==="dev_report") { //获取各种状态
            console.log("dev_report");
            if (result.data != undefined) {
                var data = result.data;
                console.log(data);
                if (data.dev_class_type === "light") {
                    obj.light(data);
                }
                if (data.dev_class_type === "curtain"){
                    obj.curtain(data);
                }
                if(data.msg_type==="security_mode_change"&&data.command==="up"){
                    var mode=data.security_mode;
                    switch (mode){
                        case "home":
                            $("#dropdownmenu_safety").find('img').attr("src",obj.baseurl+'blog/img/smarthome/safety_home.png');
                            break;
                        case "out":
                            $("#dropdownmenu_safety").find('img').attr("src",obj.baseurl+'blog/img/smarthome/safety_out.png');
                            break;
                        case "sleep":
                            $("#dropdownmenu_safety").find('img').attr("src",obj.baseurl+'blog/img/smarthome/safety_sleep.png');
                            break;
                        case "disarm":
                            var gesturepwd_window = document.getElementById('gesturepwd_window');
                            var over = document.getElementById('over');
                            gesturepwd_window.style.display = "none";
                            over.style.display = "none";
                            $("#dropdownmenu_safety").find('img').attr("src",obj.baseurl+'blog/img/smarthome/safety_disarm.png');
                            break;
                        default :
                            $("#dropdownmenu_safety").find('img').attr("src",obj.baseurl+'blog/img/smarthome/safety_home.png');
                    }
                }
            }
        }
        if(result.cmd==="send_msg"&&result.subject==="control") //获取设备、房间、场景
        {
            if (result.msg != undefined && result.msg != null) {
                var msg = JSON.parse(result.msg);
                if (msg.result === "success") {
                    if (msg.msg_type === "room_manager") {
                        if (msg.rooms != undefined && msg.rooms != null) {
                            var room_obj = {"rooms": msg.rooms};
                            window.localStorage["rooms"] = JSON.stringify(room_obj);
                            console.log(window.localStorage["rooms"]);
                        }
                    }
                    if (msg.msg_type === "combination_control_manager") {
                        if (msg.combs != undefined && msg.combs != null) {
                            var comb_obj = {"combs": msg.combs};
                            window.localStorage["combs"] = JSON.stringify(comb_obj);
                            console.log(window.localStorage["combs"]);
                        }
                        if(msg.command==="start"){
                           if(msg.duration!= undefined && msg.duration != null){
                               var speed=msg.duration;
                               var control_name=msg.control_name;
                               var array_by_name=document.getElementsByName(control_name);
                               for(var i=0;i<array_by_name.length;i++){
                                     if(array_by_name[i].getAttribute("class")==="a-img2"){
                                         var canvas_obj=array_by_name[i].firstChild;
                                         console.log(canvas_obj);
                                         console.log(speed);
                                         obj.sceneCanvasDraw(canvas_obj,speed);
                                     }
                               }
                           }
                        }

                    }
                    if (msg.msg_type === "device_manager") {
                        if (msg.devices != undefined && msg.devices != null) {
                            var device_obj = {"devices": msg.devices};
                            window.localStorage["devices"] = JSON.stringify(device_obj);
                            console.log(window.localStorage["devices"]);
                        }
                    }
                }
            }
        }

        if(result.result=='someone_login'){
            //$.tooltip('该帐号在其他地方登录',5000,true,function(){
            //    window.location.href='http://'+window.location.host+'/smarthome/index.php/Login/repeatLogin';
            //});
            console.log("someone_login");
        }

        if(result.result=='token_error')
        {
            //window.location.href='http://'+window.location.host+'/smarthome/index.php/Login';
            console.log("token_error");
            obj.updateTokenTime(window.localStorage['user']);
            //return;
        }

        if(result.msg!=''&&result.msg!=undefined)
        {
            if(result.msg.type!=undefined&&result.msg.type==="message")
            {
                window.localStorage.community_badger = 1;
                obj.message(result);
                //$.ajax({
                //    url : 'http://'+window.location.host+'/smarthome/index.php/Main/addsubscript',
                //    type : "POST",
                //    dataType : "text",
                //    data : {
                //        type: "service",
                //        subtype: result.msg.data[0].messagetype
                //    },
                //    success : function(data){
                //        $.console.log(data);
                //    },
                //    error : function(error){
                //        $.console.log(error);
                //    }
                //});
                console.log("message2");
                obj.getMsg();return;
            }

        }


        if($.isFunction(callback)){
              callback(result);
        }

        if(result.result=='recv_timeout'){
            obj.count++;
        }

        if(obj.count==20)
        {
            obj.updateTokenTime(window.localStorage['user']);
            // village();
        }
        obj.getMsg();
    };

    obj.getMsg = function(){
        console.log("http://server.atsmartlife.com/getmsg");
        var token=window.localStorage["text"];
        var aesKey=window.localStorage["debug"];
        var url="http://server.atsmartlife.com/getmsg?token="+token;
        //console.log(token);
        console.log(aesKey);
        //console.log(url);
        $.ajax({
            url : url,
            type : "get",
            dataType : "text",
            success : function(data){
                try{
                    if(data==''||data==undefined)
                    {
                        return ;
                    }
                    var result = obj.aesDecrypt(data,aesKey);
                    //console.log(result);
                    obj.filterMessage(result);
                }catch (error){
                    if(error.message==='Malformed UTF-8 data'){
                        obj.updateAeskey();
                    }
                    //obj.getMsg();
                    setTimeout(obj.getMsg,3000);
                    console.log(error);
                }

            },
            error : function(error){
                console.log('request error');
                //window.location.href='http://'+window.location.host+'/smarthome/index.php/Login';
                setTimeout(obj.getMsg,3000);
                //obj.getMsg();
                console.log(error);
            }
        });
    };

    obj.getMsg();

})();