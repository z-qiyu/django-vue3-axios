import datetime
import json
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View
from copy import deepcopy
from apis.models import UserProfile, Carport, ComplaintMessage, MaintainMessage, Charge, Announcement
from apis.utils import JWT
from django.core.paginator import Paginator

status = "status"
msg = "msg"


#
# u = User.objects.create(
#     username="zqy",
#     is_superuser=True,
#     password="123456",
# )
# UserProfile.objects.create(
#     user=u,
#     telephone="13257216957",
#     gender="1",
#     user_type="3",
#     user_property={"data": ["宠物", "房子", "汽车"]}
# )


def index(req):
    res = {
        status: 200,
        msg: "status code 200 , api index"
    }
    return JsonResponse(res)


class Login(View):

    def post(self, req):
        res = {
            status: 200,
            msg: "ok"
        }
        req_data = json.loads(req.body)
        u = User.objects.filter(username=req_data["username"]).first()
        if u and u.check_password(req_data["password"]):
            req_data.pop("csrfmiddlewaretoken", None)
            req_data['user_type'] = u.profile.user_type
            res['user_type'] = u.profile.user_type
            res['token'] = JWT.get_jwt_token(req_data)
        else:
            res[status] = 201
            res[msg] = "不存在用户名 或 密码错误"
        return HttpResponse(json.dumps(res), content_type="application/json")


class Register(View):

    def post(self, req):
        res = {
            status: 200,
            msg: "ok"
        }
        req_data = json.loads(req.body)
        req_data_copy = deepcopy(req_data)
        req_data_copy.pop("user_type", None)
        if all(req_data_copy.values()):
            if req_data['password'] == req_data['re_password']:

                if User.objects.filter(username=req_data['username']):
                    res[status] = 201
                    res[msg] = "已有用户！"
                else:
                    # 维修员 & 普通用户
                    u = User(
                        username=req_data['username'],
                        email=req_data["email"],
                    )
                    u.set_password(req_data["password"])
                    u.save()
                    UserProfile.objects.create(
                        user=u,
                        telephone=req_data["tel"],
                        is_audit=not req_data["user_type"],
                        user_type="2" if req_data["user_type"] else "1",
                        gender=req_data["gender"]
                    )
            else:
                res[status] = 202
                res[msg] = "两次密码不正确!"
        else:
            res[status] = 203
            res[msg] = "没有填写必填项!"

        return HttpResponse(json.dumps(res), content_type="application/json")


class UserInfo(View):

    def dispatch(self, req, *args, **kwargs):
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            return JsonResponse({status: 201, msg: token_dict['error']})
        obj = super(UserInfo, self).dispatch(req, token_dict['data']['data']['username'], *args, **kwargs)
        return obj

    def get(self, req, username):
        res = {
            status: 200,
            msg: "ok",
            'data': {}
        }
        u = User.objects.filter(username=username).first()
        res['data']['username'] = u.username
        res['data']['email'] = u.email
        res['data']['tel'] = u.profile.telephone
        res['data']['ut'] = u.profile.get_user_type_display()
        res['data']['gender'] = u.profile.get_gender_display()
        res['data']['property'] = u.profile.user_property if u.profile.user_property else []
        res['data']['carport'] = len(u.carport.all())

        return JsonResponse(res)

    def delete(self, req, username):
        return JsonResponse({})


class GetDatas:
    @staticmethod
    def getUsers(req):
        res = {
            status: 200,
            msg: "ok",
            'data': {
                'data': [],
                "filed": [],
                "pageNum": 0
            },
        }
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            res[status] = 201
            res[msg] = token_dict['error']
            return JsonResponse(res)
        obj = Paginator(
            User.objects.all()
            if token_dict['data']['data']['user_type'] == '3'
            else User.objects.filter(username=token_dict['data']['data']['username']),
            15)
        res['data']["pageNum"] = obj.num_pages
        for u in obj.page(int(json.loads(req.body)["page"])):
            temp = {'username': u.username,
                    'email': u.email,
                    'tel': u.profile.telephone,
                    'ut': u.profile.get_user_type_display(),
                    'gender': u.profile.get_gender_display(),
                    'property': u.profile.user_property}
            res['data']['data'].append(temp)
        res['data']['filed'] = [['用户名', 'username'],
                                ['邮箱', 'email'],
                                ['电话', 'tel'],
                                ['用户类型', 'ut'],
                                ['性别', 'gender'],
                                ['资产', 'property']
                                ]
        return JsonResponse(res)

    @staticmethod
    def getCarports(req):
        res = {
            status: 200,
            msg: "ok",
            'data': {
                'data': [],
                "filed": [],
                "pageNum": 0
            }
        }
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            res[status] = 201
            res[msg] = token_dict['error']
            return JsonResponse(res)
        obj = Paginator(
            Carport.objects.all()
            if token_dict['data']['data']['user_type'] == '3'
            else Carport.objects.filter(to_user__username=token_dict['data']['data']['username'])
            , 15)
        res['data']["pageNum"] = obj.num_pages
        for c in obj.page(int(json.loads(req.body)["page"])):
            temp = {'id': f"第C-{c.id}号车位",
                    'username': c.to_user.username if c.to_user else "暂无户主",
                    'tel': c.to_user.profile.telephone if c.to_user else "暂无户主"}
            res['data']['data'].append(temp)
        res['data']['filed'] = [['车位编号', 'id'],
                                ['车位所属用户名', 'username'],
                                ['车位所属用户电话', 'tel']
                                ]
        return JsonResponse(res)

    @staticmethod
    def getComplaintMessage(req):
        res = {
            status: 200,
            msg: "ok",
            'data': {
                'data': [],
                "filed": [],
                "pageNum": 0
            }
        }
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            res[status] = 201
            res[msg] = token_dict['error']
            return JsonResponse(res)
        obj = Paginator(

            ComplaintMessage.objects.filter(to_user__username=token_dict['data']['data']['username'])
            if token_dict['data']['data']['user_type'] != '3'
            else ComplaintMessage.objects.all()

            , 15)
        res['data']["pageNum"] = obj.num_pages
        for c, idx in zip(obj.page(int(json.loads(req.body)["page"])),
                          range(len(obj.page(int(json.loads(req.body)["page"]))))):
            temp = {'meta_id': c.id,
                    'id': idx,
                    'username': c.to_user.username if c.to_user else '用户已经注销',
                    'tel': c.to_user.profile.telephone if c.to_user else '用户已经注销',
                    'time': c.update_time,
                    'msg': c.msg}
            res['data']['data'].append(temp)
        res['data']['filed'] = [['编号', 'id'],
                                ['投诉人用户名', 'username'],
                                ['投诉入电话号码', 'tel'],
                                ['投诉时间', 'time'],
                                ['投诉信息', 'msg'],
                                ]
        return JsonResponse(res)

    @staticmethod
    def getMaintainMessage(req):
        res = {
            status: 200,
            msg: "ok",
            'data': {
                'data': [],
                "filed": [],
                "pageNum": 0
            }
        }
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            res[status] = 201
            res[msg] = token_dict['error']
            return JsonResponse(res)
        obj = Paginator(
            MaintainMessage.objects.filter(to_user__username=token_dict['data']['data']['username'])
            if token_dict['data']['data']['user_type'] == '1'
            else MaintainMessage.objects.all()
            , 15)
        res['data']["pageNum"] = obj.num_pages
        for m, idx in zip(obj.page(int(json.loads(req.body)["page"])),
                          range(len(obj.page(int(json.loads(req.body)["page"]))))):
            temp = {'meta_id': m.id,
                    'id': idx,
                    'username': m.to_user.username if m.to_user else '用户已经注销',
                    'tel': m.to_user.profile.telephone if m.to_user else '用户已经注销',
                    'maintenance_men_username': m.to_maintenance_men.username if m.to_maintenance_men else '暂未维修',
                    'maintenance_men_tel': m.to_maintenance_men.profile.telephone if m.to_maintenance_men else '暂未维修',
                    'time': m.update_time,
                    'maintain_time': m.maintain_time if m.to_maintenance_men else '暂未维修',
                    'msg': m.msg}
            res['data']['data'].append(temp)
        res['data']['filed'] = [['编号', 'id'],
                                ['维修申请人用户名', 'username'],
                                ['维修申请人电话号码', 'tel'],
                                ['维修员用户名', 'maintenance_men_username'],
                                ['维修员电话号码', 'maintenance_men_te'],
                                ['维修发起时间', 'time'],
                                ['维修时间', 'maintain_time'],
                                ['维修备注', 'msg'],
                                ]
        return JsonResponse(res)

    @staticmethod
    def getCharge(req):
        res = {
            status: 200,
            msg: "ok",
            'data': {
                'data': [],
                "filed": [],
                "pageNum": 0
            }
        }
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            res[status] = 201
            res[msg] = token_dict['error']
            return JsonResponse(res)
        obj = Paginator(
            Charge.objects.all()
            if token_dict['data']['data']['user_type'] == '3'
            else Charge.objects.filter(to_user__username=token_dict['data']['data']['username'])
            , 15)
        res['data']["pageNum"] = obj.num_pages
        for m, idx in zip(obj.page(int(json.loads(req.body)["page"])),
                          range(len(obj.page(int(json.loads(req.body)["page"]))))):
            temp = {'meta_id': m.id,
                    'id': idx,
                    'username': m.to_user.username if m.to_user else '用户已经注销',
                    'tel': m.to_user.profile.telephone if m.to_user else '用户已经注销',
                    'charge_type': m.get_charge_type_display(),
                    'money': m.money,
                    'time': m.update_time}
            res['data']['data'].append(temp)
        res['data']['filed'] = [['编号', 'id'],
                                ['缴费人用户名', 'username'],
                                ['缴费人电话号码', 'tel'],
                                ['缴费类型', 'charge_type'],
                                ['缴费金额', 'money'],
                                ['缴费时间', 'time'],
                                ]
        return JsonResponse(res)

    @staticmethod
    def getAnnouncement(req):
        res = {
            status: 200,
            msg: "ok",
            'data': {
                'data': [],
                "filed": [],
                "pageNum": 0
            }
        }
        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        if token_dict['error']:
            res[status] = 201
            res[msg] = token_dict['error']
            return JsonResponse(res)

        for m in Announcement.objects.all():
            temp = {
                'meta_id': m.id,
                'title': m.title,
                'content': m.content,
                'time': m.update_time}
            res['data']['data'].append(temp)
        return JsonResponse(res)


def complaint(req):
    res = {
        status: 200,
        msg: "ok"
    }
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        res[status] = 201
        res[msg] = token_dict['error']
        return JsonResponse(res)
    try:
        ComplaintMessage.objects.create(
            to_user=User.objects.filter(username=token_dict['data']['data']['username']).first(),
            msg=req_data[msg]
        )
    except Exception:
        res[status] = 202
        res[msg] = "错误: db,联系管理员"
        return JsonResponse(res)
    return JsonResponse(res)


def maintain(req):
    res = {
        status: 200,
        msg: "ok"
    }
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        res[status] = 201
        res[msg] = token_dict['error']
        return JsonResponse(res)
    try:
        MaintainMessage.objects.create(
            to_user=User.objects.filter(username=token_dict['data']['data']['username']).first(),
            msg=req_data[msg]
        )
    except Exception as e:
        res[status] = 202
        res[msg] = "错误: db,联系管理员"
        return JsonResponse(res)
    return JsonResponse(res)


def charge(req):
    res = {
        status: 200,
        msg: "ok"
    }
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        res[status] = 201
        res[msg] = token_dict['error']
        return JsonResponse(res)
    try:
        user = User.objects.filter(username=token_dict['data']['data']['username']).first()
        if req_data['type'] == "3":
            if len(Carport.objects.filter(to_user=None)) == 0:
                res[status] = 203
                res[msg] = "车位已满,暂无车位购买"
                return JsonResponse(res)
            c = Carport.objects.filter(to_user=None).first()
            c.to_user = user
            c.save()

        Charge.objects.create(
            to_user=user,
            money=req_data['money'],
            charge_type=req_data['type']
        )

    except Exception as e:
        res[status] = 202
        res[msg] = "错误: db,联系管理员"
        return JsonResponse(res)
    return JsonResponse(res)


def announcement(req):
    res = {
        status: 200,
        msg: "ok"
    }
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        res[status] = 201
        res[msg] = token_dict['error']
        return JsonResponse(res)

    if token_dict['data']['data']['user_type'] != '3':
        res[status] = 203
        res[msg] = "当前用户不能发布公告！"
        return JsonResponse(res)
    try:
        Announcement.objects.create(
            title=req_data['title'],
            content=req_data['content']
        )
    except Exception as e:
        res[status] = 202
        res[msg] = "错误: db,联系管理员"
        return JsonResponse(res)
    return JsonResponse(res)


class DelDatas:
    # 删除路由分发
    @staticmethod
    def getDelMethodFunc(req):

        token = req.headers["Authorization"]
        token_dict = JWT.decode_jwt_token(token)
        del_id = json.loads(req.body)['id']
        if token_dict['error']:
            return JsonResponse({
                status: 201,
                msg: token_dict['error']
            })

        t = req.META['PATH_INFO'][req.META['PATH_INFO'].rindex('/') + 1:]
        if not t:
            return JsonResponse({
                status: 201,
                msg: "错误,刷新重试"
            })
        else:
            if t == 'user':
                if token_dict['data']['data']['user_type'] != '3':
                    return JsonResponse({
                        status: 205,
                        msg: "没有权限!"
                    })
                return DelDatas.User(del_id)
            if t == 'complaint':
                if token_dict['data']['data']['user_type'] == '2':
                    return JsonResponse({
                        status: 205,
                        msg: "没有权限!"
                    })
                return DelDatas.ComplaintMessage(del_id)
            if t == 'maintain':
                if token_dict['data']['data']['user_type'] == '2':
                    return JsonResponse({
                        status: 205,
                        msg: "没有权限!"
                    })
                return DelDatas.MaintainMessage(del_id)
            if t == 'charge':
                if token_dict['data']['data']['user_type'] == '2':
                    return JsonResponse({
                        status: 205,
                        msg: "没有权限!"
                    })
                return DelDatas.Charge(del_id)
            if t == 'announcement':
                if token_dict['data']['data']['user_type'] != '3':
                    return JsonResponse({
                        status: 205,
                        msg: "没有权限!"
                    })
                return DelDatas.Announcement(del_id)
        return JsonResponse({
            status: 201,
            msg: "错误,非法访问！"
        })

    @staticmethod
    def User(uid):
        obj = User.objects.filter(username=uid).first()
        return DelDatas.verify(obj)

    @staticmethod
    def ComplaintMessage(req):
        obj = ComplaintMessage.objects.filter(id=req).first()
        return DelDatas.verify(obj)

    @staticmethod
    def MaintainMessage(req):
        obj = MaintainMessage.objects.filter(id=req).first()
        return DelDatas.verify(obj)

    @staticmethod
    def Charge(req):
        obj = Charge.objects.filter(id=req).first()
        return DelDatas.verify(obj)

    @staticmethod
    def Announcement(req):
        obj = Announcement.objects.filter(id=req).first()
        return DelDatas.verify(obj)

    @staticmethod
    def verify(obj):
        if not obj:
            return JsonResponse({
                status: 204,
                msg: "不存在"
            })
        try:
            obj.delete()
            return JsonResponse({
                status: 200,
                msg: "ok"
            })
        except Exception:
            return JsonResponse({
                status: 202,
                msg: "错误: db,联系管理员"
            })


def add_property(req):
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        return JsonResponse({
            status: 201,
            msg: token_dict['error']
        })

    u = User.objects.filter(username=token_dict['data']['data']['username']).first()
    u.profile.user_property = req_data['t']
    u.profile.save()

    return JsonResponse({
        status: 200,
        msg: 'ok'
    })


def updateMaintain(req):
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        return JsonResponse({
            status: 201,
            msg: token_dict['error']
        })

    try:
        m_user = User.objects.filter(username=token_dict['data']['data']['username']).first()
        if m_user.profile.user_type != '2':
            return JsonResponse({
                status: 203,
                msg: '权限错误!'
            })
        m = MaintainMessage.objects.filter(id=req_data['id']).first()
        m.to_maintenance_men = m_user
        m.maintain_time = datetime.datetime.now()
        m.save()
    except Exception:
        return JsonResponse({
            status: 202,
            msg: 'db错误,请联系管理员'
        })

    return JsonResponse({
        status: 200,
        msg: 'ok'
    })


def offUser(req):
    token = req.headers["Authorization"]
    token_dict = JWT.decode_jwt_token(token)
    req_data = json.loads(req.body)
    if token_dict['error']:
        return JsonResponse({
            status: 201,
            msg: token_dict['error']
        })

    password = req_data['password']
    u = User.objects.filter(username=token_dict['data']['data']['username']).first()
    if u and u.check_password(password):
        try:
            u.delete()
        except Exception:
            return JsonResponse({
                status: 208,
                msg: 'db错误! 联系管理员'
            })
    else:
        return JsonResponse({
            status: 208,
            msg: '密码错误! 联系管理员'
        })
    return JsonResponse({
        status: 200,
        msg: 'ok'
    })