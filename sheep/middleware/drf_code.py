# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/10 17:43
import json
from typing import Mapping

from django.http.response import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

from apps.user.authentication import TokenAuthentication
from sheep.constant import RET


class DRFCodeMiddleware(MiddlewareMixin):
    """
    处理drf响应middleware
        使用此中间件会造成所有status_code为200状态(500错误除外)
    """

    def process_template_response(self, request, response):
        response = self.process_response(request, response)
        # 解决filter组件在drf可视化页面分页的情况下显示不出来的问题
        if not hasattr(response, 'renderer_context'):
            return response
        paginator = getattr(response.renderer_context['view'], "paginator", None)
        if paginator:
            paginator.get_results = (lambda x: x['data']['results'])
        return response

    def process_response(self, request, response):
        status_code = response.status_code
        # 500的情况
        if status_code >= 500 or response.exception:
            return response

        data = self.get_response_data(response)
        # 正常返回的情况
        if 200 <= status_code < 300:
            data = self.success_response_handle(data)
        # 500之外的情况
        else:
            data = self.error_response_handle(request, response,
                                              data, status_code)
        response.status_code = 200
        self.set_response_data(response, data)
        return response

    @staticmethod
    def set_response_data(response, data):
        if isinstance(response, Response):
            response.data = data
        else:
            response.content = json.dumps(data).encode()

    @staticmethod
    def get_response_data(response):
        if isinstance(response, Response):
            return response.data
        else:
            return json.loads(response.content)

    @staticmethod
    def success_response_handle(data):
        """无异常正常返回时"""
        if isinstance(data, Mapping)\
                and not {'code', 'data'} - set(data.keys()):
            return data
        data = {
            'success': True,
            'code': RET.OK,
            'data': data
        }
        return data

    def error_response_handle(self, request, response, data, c):
        """正常报错返回"""

        # 特殊状态处理映射
        error_dict = {
            400: self.error_400_handle,     # serializer内抛出的异常
            401: self.error_401_handle,     # token失效的异常
        }
        # 特定的几种状态处理
        if c in error_dict.keys():
            error_dict.get(c)(response, data)
        # 当报错返回数据没有包含code,success,msg关键状态
        if {'code', 'msg'} - set(data.keys()):
            data = {
                'success': False,
                'code': c,
                'msg': data.get('detail', '没有报错提示!')
            }

        data['code'] = int(data['code'])
        data['status'] = c
        return data

    @staticmethod
    def error_400_handle(response, data):
        """
        特定报错状态处理
        使用原生django的validators时候 URLValidator(message='头像地址不正确!')只能传入str,传入dict无效
        """
        # 在validate方法中的报错会没有字段名称显示
        if not {'code', 'msg'} - set(data.keys()):
            data['success'] = False
            data = {k: v[0] if isinstance(v, list) else v for k, v in data.items()}
            return data
        for field, res_msg in data.copy().items():
            error_msg = dict()
            if isinstance(res_msg, Mapping):
                # 如果报错信息是dict形式
                s, c, m = res_msg.get('success', False), res_msg.get('code', RET.PARAMERR), res_msg.get('msg')
                error_msg['success'] = s[0] if isinstance(s, list) else s
                error_msg['code'] = c[0] if isinstance(c, list) else c
                error_msg['msg'] = m[0] if isinstance(m, list) else m
            else:
                # 如果报错信息是list或者str,也就是serializer原始默认的报错
                error_msg['success'] = False
                error_msg['code'] = RET.PARAMERR
                res_msg = res_msg[0] if len(res_msg) else ""
                error_msg['msg'] = res_msg
            data = error_msg
            break
        return data

    @staticmethod
    def error_401_handle(response, data):
        response.delete_cookie(TokenAuthentication.token_name)


