import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # 类的初始化方法，接收一个get_response参数，这是一个函数，用于获取响应对象。

    def __call__(self, request):
        uid = self.generate_uid(request)  # 调用generate_uid方法生成或获取UID，然后将这个UID存储在请求对象的uid属性中
        request.uid = uid
        response = self.get_response(request)  # 调用get_response函数获取响应对象

        # 通过set_cookie方法设置cookie，其中cookie的键为USER_KEY，值为UID，最大有效时间为10年，且设置了httponly=True，表示只在服务端能访问。
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        # 尝试从请求的cookie中获取UID，如果cookie中不存在UID，则使用uuid.uuid4().hex生成一个新的UUID字符串作为UID。
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
