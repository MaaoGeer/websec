"""
URL configuration for websec project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from index import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/login/')),
    # path('user/delete/', views.user_del),
    # path('user/list/', views.user_list),
    # path('temp_learn/', views.temp_learn),
    # path('something/', views.something),
    path('login/', views.login),
    path('user/add/', views.user_add),
    path('user/manage/', views.user_manage),
    path('user/update_name/', views.update_username),
    path('user/update_password/', views.update_password),
    path('main/', views.file_main),
    path('file/upload/', views.file_add),
    path('file/delete/<int:file_id>/', views.file_delete),   # <int:file_id>表示这是一个不固定的id

]
