# -*- coding: utf-8 -*-
# @Time : 2022/9/14 12:23
# @File : urls.py

from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index),
    path("user/", include([
        path("getinfo", UserInfo.as_view()),
        path("login", Login.as_view()),
        path("register", Register.as_view()),
        path("getinfos", GetDatas.getUsers),
        path("add_property", add_property),
        path('off', offUser)
    ])),
    path("get_data/", include([
        path("carports", GetDatas.getCarports),
        path("complaintMessage", GetDatas.getComplaintMessage),
        path("maintainMessage", GetDatas.getMaintainMessage),
        path("charge", GetDatas.getCharge),
        path("announcement", GetDatas.getAnnouncement),
    ])),
    path("complaint",complaint),
    path("maintain", maintain),
    path("charge", charge),
    path("announcement", announcement),
    path("updateMaintain",updateMaintain),
    path("del_data/", include([
        path("user", DelDatas.getDelMethodFunc),
        path("complaint", DelDatas.getDelMethodFunc),
        path("maintain", DelDatas.getDelMethodFunc),
        path("charge", DelDatas.getDelMethodFunc),
        path("announcement", DelDatas.getDelMethodFunc),
    ])),
]
