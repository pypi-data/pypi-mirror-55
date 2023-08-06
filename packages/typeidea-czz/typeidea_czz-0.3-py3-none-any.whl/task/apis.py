from rest_framework import viewsets

from .models import Task, TaskCategory
from .serializers import (
    TaskSerializer, TaskDetailSerializer,
    TaskCategorySerializer, TaskCategoryDetailSerializer
)


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """ 提供文章接口 """
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(status=Task.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TaskDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        task_category_id = self.request.query_params.get('task_category')
        if task_category_id:
            queryset = queryset.filter(task_category_id=task_category_id)
        return queryset


class TaskCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskCategorySerializer
    queryset = TaskCategory.objects.filter(status=TaskCategory.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TaskCategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
