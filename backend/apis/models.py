from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# 用户
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone = models.CharField(max_length=16, blank=True)
    gender = models.CharField(max_length=4, choices=(('1', '男'), ('2', '女')))
    user_type = models.CharField(max_length=6, choices=(('1', '住户'), ('2', '维修员'), ('3', '管理员')))
    # 审核
    is_audit = models.BooleanField(default=True)
    # 个人资产
    user_property = models.JSONField(default=list)

    class Meta:
        ordering = ["id"]


# 车位信息
class Carport(models.Model):
    id = models.BigAutoField(primary_key=True)
    to_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='carport')

    class Meta:
        ordering = ["id"]


carport_num = len(Carport.objects.all())
if carport_num < 50:
    for i in range(settings.CARPORT_NUM - carport_num):
        Carport.objects.create()


# 投诉信息
class ComplaintMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    to_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="complaint")
    update_time = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=300)

    class Meta:
        ordering = ["id"]


# 维修信息
class MaintainMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    to_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="to_user")
    to_maintenance_men = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                           related_name="to_maintenance_men")
    update_time = models.DateTimeField(auto_now_add=True)
    maintain_time = models.DateTimeField(null=True)
    msg = models.CharField(max_length=300)

    class Meta:
        ordering = ["id"]


# 收费信息
class Charge(models.Model):
    id = models.BigAutoField(primary_key=True)
    to_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="charge")
    money = models.FloatField()
    charge_type = models.CharField(max_length=6, choices=(('1', '物业费'), ('2', '水费'), ('3', '车位费')))
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]


class Announcement(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=128)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-update_time"]
