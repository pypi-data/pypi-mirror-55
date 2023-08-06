from rest_framework import serializers, pagination

from .models import Task, TaskCategory


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    task_category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')

    class Meta:
        model = Task
        fields = ['url', 'id', 'task_content', 'task_category', 'tag', 'owner', 'created_time', 'task_status']
        extra_kwargs = {
            'url': {'view_name': 'api-task-detail'}
        }


class TaskDetailSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_content', 'task_category', 'tag', 'owner', 'content_html', 'created_time', 'task_status']


class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = (
            'id', 'name', 'created_time'
        )


class TaskCategoryDetailSerializer(TaskCategorySerializer):
    tasks = serializers.SerializerMethodField('paginated_tasks')

    def paginated_tasks(self, obj):
        tasks = obj.task_set.filter(status=Task.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(tasks, self.context['request'])
        serializer = TaskSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': tasks.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = TaskCategory
        fields = (
            'id', 'name', 'created_time', 'tasks'
        )
