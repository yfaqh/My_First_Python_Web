"""Yh_web URL Configuration

The `urlpatterns`  routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views., name='')
Class-based views
    1. Add an import:  from other_app.views import 
    2. Add a URL to urlpatterns:  path('', .as_view(), name='')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    # 主页
    path('', views.home),
    path('post/list/', views.home),
    # 发表新帖
    path('post/create/', views.create_post),
    # 阅读帖子
    path('post/read/', views.read_post),
    # 发表评论
    path('post/comment/', views.comment),
    # 删除评论
    path('post/del_comment/', views.Delete_Comment),
    # 编辑帖子
    path('post/edit/', views.Edit_Post),
    # 删除帖子
    path('post/delete/', views.Delete_Post),


    # 注册
    path('user/register/', views.register),
    # 登录
    path('user/login/', views.login),
    # 注销
    path('user/logout/', views.logout),
    # 用户信息
    path('user/info/', views.user_info),
    # 用户列表
    path('users/list/', views.users_list),
    # 刷新用户信息列表
    path('refresh/info/', views.users_list),
    # 生成验证码
    path('index/verification_code/', views.verification_code),
    # 显示验证码
    path('show_verify/', views.login),
    # 更改头像
    path('img/modify/', views.Img_Modify),
    # 显示某个人的信息
    path('show/somebody/', views.Show_somebody),

    # 未完成
    path('unfinish/', views.Unfinish)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
