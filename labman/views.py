import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from labman.serializers import *


# 登录
class LoginView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response()
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if not all([username, password]):
            return Response({'detail': '用户名或密码为空'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response()


# 注销
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        logout(request)
        return Response()


# 注册
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if not all([username, password]):
            return Response({'detail': '用户名或密码为空'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).first():
            return Response({'detail': '用户名已被使用'}, status=status.HTTP_400_BAD_REQUEST)
        if ' ' in password:
            return Response({'detail': '密码不可包含空格'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response()


# 用户信息
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# 公告列表
class NoticesView(APIView):
    def get(self, request):
        notices = Notice.objects \
            .order_by('-priority', '-publish_time') \
            .all()
        if request.GET.get('all') is None:
            notices = notices.filter(priority__gt=0)
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        title = data.get('title')
        content = data.get('content')
        priority = data.get('priority')
        Notice.objects.create(title=title, content=content, priority=priority, publisher=user)
        return Response()


# 公告操作
class NoticeView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, notice_id):
        notice = get_object_or_404(Notice, id=notice_id)
        serializer = NoticeSerializer(notice)
        return Response(serializer.data)

    def put(self, request, notice_id):
        notice = get_object_or_404(Notice, id=notice_id)
        user = request.user
        data = request.data
        notice.title = data.get('title')
        notice.content = data.get('content')
        notice.priority = data.get('priority')
        notice.publisher = user
        notice.save()
        return Response()

    def delete(self, request, notice_id):
        notice = get_object_or_404(Notice, id=notice_id)
        notice.delete()
        return Response()


# 获取一言
class QuoteView(APIView):
    def get(self, request):
        url = "https://v1.hitokoto.cn?c=k&c=i&encode=json"
        response = requests.get(url)
        data = response.json()
        return Response({'text': data['hitokoto'], 'author': data['from_who']})
