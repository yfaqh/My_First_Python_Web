import datetime
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponseRedirect,HttpResponse
import io

from app.models import User, Post, Comment
from app.verification import VerificationCode

# Create your views here.


# 论坛主页
def home(request):
    # 获取所有的帖子对象，最新的排在前面
    posts = Post.objects.all().order_by('-created')
    # 默认显示最新的十篇
    top_10 = Post.objects.order_by('-created')[:10]
    context = {
        'posts':posts,
        'top_10':top_10,
        'flag':'hot'
        }
    if request.method == 'POST':
        if 'hot' in request.POST:
            top_10 = Post.objects.order_by('-created')[:10]
            context = {
                'posts':posts,
                'top_10':top_10,
                'flag':'hot'
                }
            return render(request, 'post_list.html', context)
            pass

        if 'hot_viewed' in request.POST:
            # 获取浏览量前十的帖子的对象
            top_10 = Post.objects.order_by('-n_viewed')[:10]
            context = {
                'posts':posts,
                'top_10':top_10,
                'flag':'hot_viewed'
                }
            return render(request, 'post_list.html', context)
            pass
        if 'hot_commented' in request.POST:
            # 获取评论量前十的帖子的对象
            top_10 = Post.objects.order_by('-n_commented')[:10]
            context = {
                'posts':posts,
                'top_10':top_10,
                'flag':'hot_commented'
                }
            return render(request, 'post_list.html', context)
            pass
        pass
    else:
        return render(request, 'post_list.html', context)
        pass
    pass

# 界面跳转函数
def Page_Jump(request, flag_01):    # , flag_02
    action = ['安全退出成功', '注册成功', '进行评论需要先进行登录']
    page_name = '登录'
    # page = ['/user/login/', '/post/read/']
    context = {
        'action':action[flag_01],
        'page_name':page_name,
        # 'page':page[flag_02]
    }
    return render(request, 'page_jump.html', context)
    pass

# 注册主页
def register(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        password = request.POST['password']
        password2 = request.POST['password2']
        sex = request.POST['sex']
        avatar = request.FILES['avatar']
        age = int(request.POST['age'])

        if not nickname or not password:
            return render(request, 'register.html', {'error':'昵称或密码不能为空！请进行输入！'})
            pass

        if password != password2:
            return render(request, 'register.html', {'error':'两次密码不一样，请重新输入！'})
            pass

        try:
            user =User.objects.create(
                nickname = nickname,
                password = password,
                avatar = avatar,
                sex = sex,
                age = age
            )
        except IntegrityError:
            return render(request, 'register.html', {'error':'用户名已经存在，请重新输入！'})
        
        # 注册成功进入登录界面，1表示登录跳转
        return Page_Jump(request, 1)
        # return redirect('/page/jump/')
        pass
    else:
        return render(request, 'register.html')
        pass
    pass

def verification_code(request):
    text, img = VerificationCode().gene_code()
    # 存session 参考：http://www.cnblogs.com/liuye1990/p/9663474.html
    request.session['verification_code'] = text
    # img.show()  # 显示一下效果
    stream = io.BytesIO()    # 创建一个io对象
    img.save(stream, "png")    # 将图片对象im保存到stream对象里
    # stream.getvalue() 图片二级制内容，再通过HttpResponse封装，返回给前端页面
    return HttpResponse(stream.getvalue())

# 登录界面
def login(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        password = request.POST['password']

        # 1.获取post请求当中的输入验证码的内容
        verify = request.POST.get('verify')
        print("===============")
        print(verify)
        print(type(verify))
        # 2.获取浏览器请求当中的session中的值
        verifycode = request.session.get('verification_code')
        print(type(verifycode))
        print("======")
        print(verifycode)  

        if not nickname or not password:
            return render(request, 'login.html', {'error':'昵称或密码不能为空，请输入！'})
            pass
        
        if not verify:
            return render(request, 'login.html', {'error':'请输入验证码！'})
            pass
        
        try:
            user = User.objects.get(nickname=nickname)
        except IntegrityError:
            return render(request, 'login.html', {'error':'用户名不存在，请重新输入！'})

        # 验证密码和验证码
        if user.password == password:
            if verify.lower() == verifycode.lower():
                # 使用 session 机制记录登录状态
                request.session['uid'] = user.id
                request.session['nickname'] = user.nickname
                request.session['avatar'] = user.avatar.url
                user.save()
                return redirect('/post/list/')
                pass
            else:
                return render(request, 'login.html', {'error':'验证码错误，请重新输入！'})
                pass
            pass
        else:
            return render(request, 'login.html', {'error':'密码错误，请重新输入！'})
            pass
    else:
        return render(request, 'login.html')
    pass

def Show_verify(request):
    return render(request, 'login.html')
    pass

# 显示用户信息
def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html',{'user':user})
    pass

# 显示所有用户信息
def users_list(request):
    user = User.objects.all()
    return render(request, 'users_list.html', {'user':user})
    pass

# 显示某个人的信息
def Show_somebody(request):
    user = User.objects.all()
    return render(request, 'users_list.html', {'user':user})
    pass

# 修改头像
def Img_Modify(request):
    if request.method == 'POST':
        user_avatar = request.FILES['user_avatar']
        print("-=====================")
        print(type(user_avatar))
        print(user_avatar)
        # 获取到当前登录的用户
        uid = request.session['uid']
        user = User.objects.get(id=uid)
        # 更改头像
        user.avatar = user_avatar
        # 保存修改
        user.save()
        # 修改session中缓存的旧头像
        request.session['avatar'] = user.avatar.url
        return redirect('/post/list/')
        pass
    else:
        return render(request, 'user_info.html', {'error':'图像修改失败！'})
        pass
    pass

# 安全退出
def logout(request):
    request.session.flush()
    # 退出登录。0表示退出跳转
    return Page_Jump(request, 0)
    pass

# 编写帖子
def create_post(request):
    uid = request.session.get('uid', '')
    # 检查是否登录
    if not uid:     # 未登录
        error = '发帖前请先登录或注册！'
        return render(request, 'login.html', {'error':error})
        # return redirect('/user/login/', {'error':error})
        pass
    else:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            # 获取当前用户
            uid = request.session['uid']
            user = User.objects.get(id=uid)

            # 创建帖子
            post = Post.objects.create(
                title = title,
                content = content,
                author = user
            )
            return redirect('/post/read/?post_id=%s' % post.id)
            pass
        else:
            return render(request, 'post_create.html')
            pass
    pass

# 编辑帖子
def Edit_Post(request):
    if request.method == 'POST':
        # 获取到当前要编辑的帖子的id
        post_id = int(request.POST['post_id'])
        # 找到数据库里需要编辑的帖子
        post = Post.objects.filter(id=post_id)
        # 进行帖子标题和内容的更新
        post.update(
            title = request.POST['title'],
            content = request.POST['content']
        )
        return redirect('/post/read/?post_id=%d' % post_id)
        pass
    else:
        # 获取当前帖子的id
        post_id = request.GET['post_id']
        post = Post.objects.get(id=post_id)
        return render(request, 'post_edit.html', {'post':post})
        pass
    pass

# 删除帖子
def Delete_Post(request):
    # 获取到当前帖子对象
    post_id = int(request.GET['post_id'])
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/post/list/')
    pass

# 阅读评论帖子
def read_post(request):
    post_id = int(request.GET['post_id'])
    post = Post.objects.get(id=post_id)

    # 获取当前年份
    now_year = datetime.datetime.now().year
    # 计算出B龄
    B_age = now_year - post.author.created.year
    # 获取楼主最新发布的五篇帖子
    recent_posts = Post.objects.filter(author=post.author).order_by('-created')[:5]

    # 获取当前用户的在session中的uid
    uid = request.session.get('uid', '')

    # 更新浏览量，判断看帖人是不是作者本人，本人不增加浏览量
    if post.author.id != uid:
        post.n_viewed += 1
        post.save()
        pass

    # 判断当前是否有用户存在
    if not uid:     # 若当前没有用户登录，不传入user对象，不会显示删除评论的选项
        # 获取当前帖子的所有评论
        comments = Comment.objects.filter(post=post)
        tip = ' '
        context = {
            'post':post,
            'comments':comments,
            'tip':tip,
            'B_age':B_age,
            'recent_posts':recent_posts
            }
        return render(request, 'post_read.html', context)
        pass
    else:       # 若当前有用户存在，则获取user，进一步显示删除评论权限
        # 获取当前用户
        uid = request.session['uid']
        user = User.objects.get(id=uid)
        # 获取当前帖子的所有评论，并将最新的评论放在最上面
        comments = Comment.objects.filter(post=post).order_by('-created')
        context = {
            'post':post,
            'comments':comments,
            'user':user,
            'B_age':B_age,
            'recent_posts':recent_posts
            }
        return render(request, 'post_read.html', context)
        pass
    pass

# 发表评论
def comment(request):
    uid = request.session.get('uid', '')
    if not uid:
        return Page_Jump(request, 2)
        pass

    content = request.POST['content']
    # 获取当前用户
    uid = request.session['uid']
    user = User.objects.get(id=uid)

    post_id = int(request.POST['post_id'])
    post = Post.objects.get(id=post_id)

    # 更新评论量，判断看帖人是不是作者本人，本人不增加评论量
    if post.author.id != uid:
        post.n_commented += 1
        post.save()
        pass
    
    Comment.objects.create(
        content = content,
        author = user,
        post = post
    )

    return redirect('/post/read/?post_id=%s' % post.id)
    pass

# 删除评论
def Delete_Comment(request):
    # 获取当前用户
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    # 获取到当前帖子对象
    post_id = request.GET['post_id']
    post = Post.objects.get(id=post_id)

    comment_id = request.GET['comment_id']
    Comment.objects.get(id=comment_id).delete()

    if post.author.id != uid:
        post.n_commented -= 1
        post.save()
        pass
    
    return redirect('/post/read/?post_id=%s' % post.id)
    pass


# 未完成页面
def Unfinish(request):
    return render(request, 'unfinish.html')
    pass
