import datetime

import jwt
from jwt import exceptions

headers = {
    "type": "jwt",
    "alg": "HS256"
}
JWT_SALT = "7816yediuashd78o['-d9[-'ADsdfjsdkl8qw"


class JWT:

    @staticmethod
    def get_jwt_token(payload):
        token = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'data': payload
        }
        encoded_jwt = jwt.encode(payload=token, key=JWT_SALT, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def decode_jwt_token(token):
        result = {"status": False, "data": None, "error": None}
        try:
            # 进行解密
            verified_payload = jwt.decode(token, JWT_SALT, algorithms=['HS256'])
            result["status"] = True
            result['data'] = verified_payload
        except exceptions.ExpiredSignatureError:
            result['error'] = 'token已失效'
        except jwt.DecodeError:
            result['error'] = 'token认证失败'
        except jwt.InvalidTokenError:
            result['error'] = '非法的token'
        return result
