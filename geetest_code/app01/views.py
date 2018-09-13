from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from geetest import GeetestLib
from django.contrib import auth
# Create your views here.
#报错出现requests不存在，直接注释即可

def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        username = request.POST.get('username')
        password = request.POST.get('password')
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(request,username=username,password=password)
            if user:
                # 用户名密码正确
                # 登录
                auth.login(request,user)
                ret['msg'] = '/index/'
            else:
                # 用户名密码错误
                ret["status"] =1
                ret['msg'] = "用户名或密码错误"
        else:
            # 验证码不正确
            ret["status"] = 1
            ret['msg'] = "验证码错误"

        return JsonResponse(ret)
    return render(request,'login2.html')
pc_geetest_id = "7fccd975dea97df91a7656807a103ea9"
pc_geetest_key = "ccee73093bd10be780dad0816cc2c895"
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

def index(request):
    return render(request, 'index.html')