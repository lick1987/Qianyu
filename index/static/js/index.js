$(function () {
    $("#header li").mouseover(function () {
        $("#header li>a").eq($(this).index()).css("color","red");
    })
     $("#header li").mouseout(function () {
        $("#header li>a").eq($(this).index()).css("color","white");
    })
     //点击登录事件
    $(".login:eq(0)").click(function(){
        var $div=$("<div></div>");
        $div.attr('class','mask');
        $div.attr('id','mask');
        $("body").append($div);
        $("#dialog").css("display","block")
    })
    //点击x按钮
    $(".closeBtn:eq(0)").click(function(){
        $("#dialog:eq(0)").css("display","none")
        $(".mask:eq(0)").remove()
    })
    //用户名失去焦点事件
    $('.text:eq(0)').blur(function () {
        if($('.text:eq(0)').val()){
              $('.t:eq(0)').css('display','none')
        }else{
           $('.t:eq(0)').text('用户名不能为空')
           $('.t:eq(0)').css('display','block')}
        })
    //用户输入密码失去焦点事件
    $('.text:eq(1)').blur(function () {
        if($('.text:eq(1)').val()){
              $('.t:eq(0)').css('display','none')
        }else{
           $('.t:eq(0)').text('密码不能为空')
           $('.t:eq(0)').css('display','block')}
        })
    // 绑定submit登录事件全为空不能登录
    $('#formReg').submit(function(){
        if($('.text:eq(0)').val()&&$('.text:eq(1)').val()){
            return true
        }
        return false
    })
    //绑定内容输入文本框失去焦点事件
    $('.input_text').blur(function(){
        $('#text').attr('value',$('.input_text').val());
    });
    //设置点击提交时间
    $("#button").click(function(){
        check_login()
    });
    $("#submitUnit").click(function(){
        check_add();
    });


})
 function check_login() {
            $.ajax({
                    'url':'/checkLogin',
                    'type':'POST',
                    'data':{
                        'uname':$('#uname').val(),
                        'upwd':$('#upwd').val(),
                        'isSaved':$('#isSaved').is(':checked'),
                        csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
                        },
                    'dataType':'json',
                    'success':function (data) {
                        if(data.status==1){
                            $("#dialog").css("display","none");
                            html="<a href='#'>"+data.message+"</a>"
                            html+="<a href='/exit'>退出</a>";
                            $("#useload").html(html);
                            $("#mask").css("display","none");
                            }
                        else{
                            $("#t").css("display","block");
                            }

                        }
                    });
            }
 function check_add() {
            $.ajax({
                    'url':'/addUnit',
                    'type':'POST',
                    'data':{
                        'uname':$('#uname1').val(),
                        'upwd':$('#upwd1').val(),
                        csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
                        },
                    'dataType':'json',
                    'success':function (data) {
                        if(data.status==1){
                            html=data.message;
                            $('#mes').html(html);
                            $("#mes").css("display","block");
                            $("#mes").css("color","red");
                            $('#uname1').val("");
                            $('#upwd1').val("");

                            }
                        else{
                            html=data.message;
                            $("#mes").html(html);
                            $("#mes").css("display","block");
                            $("#mes").css("color","blue");
                            $('#uname1').val("");
                            $('#upwd1').val("");
                            }

                        }
                    });
            }
