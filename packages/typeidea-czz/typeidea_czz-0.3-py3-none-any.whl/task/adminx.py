import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container

from django.urls import reverse
from django.utils.html import format_html

from .adminforms import TaskAdminForm
from .models import Task, TaskCategory, TaskTag
from typeidea.base_admin import BaseOwnerAdmin


class TaskInline:
    form_layout = (
        Container(
            Row("task_content", "task_comments"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Task


@xadmin.sites.register(Task)
class TaskAdmin(BaseOwnerAdmin):
    form = TaskAdminForm
    list_display = [
        'task_content', 'task_category', 'task_status', 'color_state',
        'responsible','raised_date','operator','owner',
    ]
    list_display_links = []

    list_filter = ['task_category', 'task_status', 'responsible', 'raised_date', 'target_date', 'closed_date',
                   'task_no']
    search_fields = ['task_content', ]
    save_on_top = True

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    exclude = ['owner']
    form_layout = (
        Fieldset(
            '基础信息',
            Row("task_content", "task_category" ),
            'status',
            'tag',
            'task_status',
        ),
        Fieldset(
            '内容信息',
            'task_comments',
            'is_md',
            'content_ck',
            'content_md',
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:task_task_change', args=(obj.id,))
        )
    operator.short_description = '操作'


    # def get_media(self):
        # # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
        # media = super().get_media()
        # media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
        # media.add_css({
            # 'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        # })
        # return media


@xadmin.sites.register(TaskCategory)
class TaskCategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'task_count', )
    fields = ('name', 'status', 'is_nav')

    def task_count(self, obj):
        return obj.task_set.count()

    task_count.short_description = '任务数量'


@xadmin.sites.register(TaskTag)
class TaskTagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class TaskCategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'task_category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = TaskCategory.objects.filter(owner=request.user).values_list('id', 'name')



manager.register(TaskCategoryOwnerFilter, take_priority=True)



