import logging
from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404, render, HttpResponse



from config.models import SideBar
from .models import Task, TaskCategory, TaskTag

logger = logging.getLogger(__name__)


class TaskCommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    def get_navs(self):
        categories = TaskCategory.objects.filter(status=TaskCategory.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class TaskIndexView(TaskCommonViewMixin, ListView):
    queryset = Task.objects.filter(status=Task.STATUS_NORMAL) \
        .select_related('owner')\
        .select_related('task_category')
    paginate_by = 10
    context_object_name = 'task_list'
    template_name = 'task/list.html'


class TaskCategoryView(TaskIndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_category_id = self.kwargs.get('task_category_id')
        task_category = get_object_or_404(TaskCategory, pk=task_category_id)
        context.update({
            'task_category': task_category,
        })
        return context

    def get_queryset(self):
        """ 重写querset，根据分类过滤 """
        queryset = super().get_queryset()
        task_category_id = self.kwargs.get('task_category_id')
        return queryset.filter(task_category_id=task_category_id)


class TaskTagView(TaskIndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(TaskTag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写querset，根据标签过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class TaskDetailView(TaskCommonViewMixin, DetailView):
    queryset = Task.objects.filter(status=Task.STATUS_NORMAL)
    template_name = 'task/detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效

        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效

        if increase_pv and increase_uv:
            Task.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Task.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Task.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class TaskSearchView(TaskIndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(task_content__icontains=keyword) | Q(task_comments__icontains=keyword)\
                               | Q(responsible__icontains=keyword))


class TaskAuthorView(TaskIndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class TaskKpiView(TaskCommonViewMixin, ListView):
    context_object_name = 'catchtask'
    template_name = 'task/render.html'
    queryset = Task.objects.filter(status=Task.STATUS_NORMAL)




# class Handler404(CommonViewMixin, TemplateView):
#     template_name = '404.html'
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context, status=404)
#
#
# class Handler50x(CommonViewMixin, TemplateView):
#     template_name = '50x.html'
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context, status=500)
