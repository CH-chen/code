from django.conf.urls import url
from django.contrib import admin
from app02 import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^reg/', views.register),
    url(r'^index/', views.index),
    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', views.get_geetest),



]