from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from apps.other.serializer import UploadSerializer, OptionSerializer, FeedbackCategorySerializer, ListFeedbackSerializer, CreateFeedbackSerializer, UpdateFeedbackSerializer
from apps.other.filters import FeedbackFilter, UploadHistoryFilter
from apps.other.models import UploadHistoryModel, Feedback, FeedbackCategory
from apps.user.permission import IsLoginUser, IsAdminUser
from utils.viewsets import ModelViewSet
from utils.pagination import LimitOffsetPagination


class UploadViewSet(GenericViewSet,
                    ListModelMixin,
                    CreateModelMixin):
    """上传文件视图"""
    pagination_class = LimitOffsetPagination
    serializer_class = UploadSerializer
    permission_classes = ()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = UploadHistoryFilter
    filter_fields = ('user_id', 'url')
    ordering_fields = "__all__"
    queryset = UploadHistoryModel.objects.all()


class OptionViewSet(GenericViewSet):
    """公共配置"""
    serializer_class = OptionSerializer
    permission_classes = ()
    queryset = ' '

    def list(self, request, *args, **kwargs):
        # raise 2/0
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data)


class FeedbackCategoryViewSet(ModelViewSet):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer

    def get_permissions(self):
        if self.request.method.lower() == 'get':
            return []
        return [IsAdminUser()]


class FeedbackViewSet(ModelViewSet):
    serializer_class = {
        'list': ListFeedbackSerializer,
        'retrieve': ListFeedbackSerializer,
        'create': CreateFeedbackSerializer,
        'update': UpdateFeedbackSerializer,
        'partial_update': UpdateFeedbackSerializer
    }
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = FeedbackFilter
    search_fields = ('desc',)
    ordering_fields = ('create_time',)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return []
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Feedback.objects.all()
        else:
            return Feedback.objects.filter(author_id=user.id).all()
