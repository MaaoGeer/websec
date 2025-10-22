from datetime import datetime

from django.shortcuts import render, redirect
from index.models import UserInfo, FileInfo
# Create your views here.
from django.shortcuts import render, HttpResponse


# Create your views here.

# 用户注册
def user_add(request):
    if request.method == "GET":
        return render(request, "user_add.html")

    # 2. 如果是 POST 请求：处理登录表单提交的数据
    elif request.method == "POST":
        # 获取表单提交的用户名和密码（从 request.POST 中获取）
        post_data = request.POST
        username = post_data.get('username').strip()
        pwd = post_data.get('password').strip()

        if not username or not pwd:
            msg_type = 'error'
            msg = '用户名或密码不能为空'
            return render(request, "user_add.html", {'msg_type': msg_type, 'msg': msg})

        user_confirm = UserInfo.objects.filter(name=username).first()
        if user_confirm:
            msg_type = 'error'
            msg = '用户已存在'
            return render(request, "user_add.html", {'msg_type': msg_type, 'msg': msg})

        UserInfo.objects.create(name=username, password=pwd)
        if UserInfo.objects.filter(name=username):
            msg_type = 'success'
            msg = '注册成功！即将跳转到登录页...'
            return render(request, "login.html", {'msg_type': msg_type, 'msg': msg})


# def user_del(request):
#     return HttpResponse('用户删除')


# def user_list(request):
#     all_data = UserInfo.objects.all()
#     # 第一个位子是视图函数的request参数，第二个参数位是html文件路径
#     return render(request, "user_list.html", {'user_list': all_data})


# def temp_learn(request):
#     name = 'zm'
#     students = 'zm'
#     #  render的第三个参数必须为   字典类型;可强制转换
#     return render(request, "temp_learn.html", {"n1": name, "stu_list": students})


# def something(request):
#     print(request.method)
#     print(request.GET)
#     print(request.POST)
#     return render(request, 'temp_learn.html')


def login(request):
    # 1. 如果是 GET 请求：展示登录页面
    if request.method == "GET":
        # 渲染登录页面模板（假设模板名为 login.html）
        return render(request, "login.html")

    # 2. 如果是 POST 请求：处理登录表单提交的数据
    elif request.method == "POST":
        # 获取表单提交的用户名和密码（从 request.POST 中获取）
        post_data = request.POST
        username = post_data.get('user')
        pwd = post_data.get('pwd')

        user = UserInfo.objects.filter(name=username).first()
        if not user:  # 用户名不存在
            return render(request, 'login.html', {'trip': '用户名或密码错误'})
        if pwd == user.password:
            request.session['user_name'] = username
            return redirect('/main/')  # 跳到主界面
        else:
            return render(request, 'login.html', {'trip': '用户名或密码错误'})


def user_manage(request):
    user = request.session.get('user_name')
    if not user:
        return redirect('/login/')

    if request.method == 'GET':
        return render(request, 'user_manage.html', )


def update_username(request):
    if request.method != 'POST':
        return redirect('/user/manage/')

    current_user = request.session.get('user_name')
    if not current_user:
        return redirect('/login/')

    # 接收前端提交的参数
    new_username = request.POST.get('new_username', '').strip()
    password = request.POST.get('password', '').strip()
    user_obj = UserInfo.objects.filter(name=current_user).first()

    if UserInfo.objects.filter(name=new_username).exists():
        return redirect('/user/manage/?username_error=该用户名已被占用，请更换')

    if password != user_obj.password:
        return redirect('/user/manage/?password_error=密码错误，请重新输入')
    else:
        UserInfo.objects.filter(name=current_user).update(name=new_username)
        FileInfo.objects.filter(upload_user=current_user).update(upload_user=new_username)
        request.session['user_name'] = new_username
        return redirect('/user/manage/')


def update_password(request):
    if request.method != 'POST':
        return redirect('/user/manage/')

    current_user = request.session.get('user_name')
    if not current_user:
        return redirect('/login/')

    # 接收前端提交的参数
    new_username = request.POST.get('new_username', '').strip()
    old_password = request.POST.get('old_password', '').strip()
    new_password = request.POST.get('new_password', '').strip()
    user_obj = UserInfo.objects.filter(name=current_user).first()

    if old_password != user_obj.password:
        return redirect('/user/manage/?password_error=密码错误，请重新输入')
    else:
        UserInfo.objects.filter(name=current_user).update(password=new_password)

        return redirect('/user/manage/')


def file_main(request):
    if not request.session.get('user_name'):  # 假设登录时保存了user_id到session
        return redirect('/login/')
    user = request.session.get('user_name')

    # 3. 查询当前用户上传的所有文件（关联FileInfo模型的upload_user字段）
    file_list = FileInfo.objects.filter(upload_user=user).order_by('-upload_time')  # 按上传时间倒序

    # 4. 传递文件列表到模板
    return render(request, 'file_main.html', {'file_list': file_list})


def file_add(request):
    user = request.session.get('user_name')
    file_list = FileInfo.objects.filter(upload_user=user).order_by('-upload_time')
    if request.method == 'POST':
        # 从 request.FILES 中获取上传的文件（单文件）
        # 注意：name 属性需与表单中 input 的 name 一致（即 "file"）
        file_obj = request.FILES.get('file')

        # 如果是多文件上传（表单中 input 有 multiple 属性），用 getlist 获取所有文件
        # file_objs = request.FILES.getlist('file')  # 返回文件对象列表

        if file_obj:
            # 获取文件名（包含扩展名）
            file_name = file_obj.name
            if file_list.filter(file_name=file_name).exists():
                now = datetime.now()
                fsize = round(file_obj.size / 1024)
                FileInfo.objects.filter(file_name=file_name).update(upload_time=now, file_size=fsize)
                file_list = FileInfo.objects.filter(upload_user=user).order_by('-upload_time')
                return redirect('/main/')
            else:
                now = datetime.now()
                fsize = file_obj.size / 1024
                FileInfo.objects.create(file_name=file_name, file_size=fsize, upload_time=now, upload_user=user)
                file_list = FileInfo.objects.filter(upload_user=user).order_by('-upload_time')
                return redirect('/main/')
        else:
            return HttpResponse("请选择文件后上传")
    else:
        # 处理 GET 请求（例如返回上传页面）
        return render(request, 'file_main.html', {'file_list': file_list})


def file_delete(request, file_id):
    # 1. 验证用户是否登录（从session获取用户名，与你的登录逻辑一致）
    user = request.session.get('user_name')
    file = FileInfo.objects.filter(id=file_id)

    if not user:
        return render(request, 'login.html')

    if not file:
        file_list = FileInfo.objects.filter(upload_user=user).order_by('-upload_time')
        return redirect('/main/')
    else:
        FileInfo.objects.filter(id=file_id).delete()
        file_list = FileInfo.objects.filter(upload_user=user).order_by('-upload_time')
        return redirect('/main/')
