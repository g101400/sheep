from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from utils.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from utils.viewsets import ExtensionViewMixin
from sheep import settings
from apps.user.serializer import ListCreateUserSerializer, LoginSerializer, DeleteUserSerializer, \
    UpdateUserSerializer, PwdSerializer
from sheep.constant import RET
from apps.user.tasks import after_user_create

User = get_user_model()


class LoginViewSet(CreateModelMixin, GenericViewSet):
    """登录视图"""
    serializer_class = LoginSerializer
    permission_classes = ()

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """登录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # response_data = jwt_response_payload_handler(token, user, request)
        headers = self.get_success_headers(serializer.data)
        data = {"success": True, "code": RET.OK, "msg": "登录成功", "data": serializer.data}
        res = Response(data, status=200, headers=headers)
        # 线上环境不设置cookie，因为有概率会覆盖nuxt的cookie设置
        if settings.DEBUG:
            res.set_cookie(settings.TOKEN.get('TOKEN_NAME'),
                           serializer.data.get('token'),
                           expires=settings.TOKEN.get('TOKEN_EXPIRS'),
                           httponly=True)
        return res

    def bulk_delete(self, request, *args, **kwargs):
        """退出登录"""
        serializer = self.get_serializer_class()
        serializer.delete(request)
        data = {"success": True, "code": RET.OK, "data": "退出登录"}
        return Response(data, status=200)

    def get_permissions(self):
        # 用户退出登录前必须先要登录
        if self.request.method == 'DELETE':
            return [temp() for temp in api_settings.DEFAULT_PERMISSION_CLASSES]
        return [temp() for temp in self.permission_classes]


class UserViewSet(CreateModelMixin,
                  ExtensionViewMixin,
                  GenericViewSet,
                  ):
    """用户个人信息"""
    serializer_class = {'list': ListCreateUserSerializer,
                        'create': ListCreateUserSerializer,
                        'bulk_delete': DeleteUserSerializer,
                        'bulk_update': UpdateUserSerializer,
                        'bulk_partial_update': UpdateUserSerializer,
                        }
    permission_classes = ()

    def get_queryset(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data)

    def get_permissions(self):
        # 只有注册时才不需要进行认证
        if self.request.method not in ['POST', "GET"]:
            return [temp() for temp in api_settings.DEFAULT_PERMISSION_CLASSES]
        return [temp() for temp in self.permission_classes]

    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(self.get_queryset(), data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # serializer.save()
        data = {"success": True, "code": RET.OK, "msg": "修改成功", "data": serializer.data}
        return Response(data)

    def bulk_partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.bulk_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def bulk_delete(self, request, *args, **kwargs):
        """注销账号"""
        serializer = self.get_serializer(self.get_queryset(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete(request.user)
        data = {"success": True, "code": RET.OK, "data": "注销成功"}
        return Response(data, status=200)

    def perform_create(self, serializer):
        instance = serializer.save()
        after_user_create.delay(instance.id)


class PwdViewSet(CreateModelMixin,
                 ExtensionViewMixin,
                 GenericViewSet):
    """修改密码"""
    serializer_class = {
        'create': PwdSerializer,
    }
