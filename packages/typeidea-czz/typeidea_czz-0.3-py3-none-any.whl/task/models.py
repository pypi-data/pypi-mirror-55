# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mistune

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.html import format_html


class TaskCategory(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="责任人", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '部门'

    def __str__(self):
        return self.name


class TaskTag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="责任人", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    TASK_STATUS_R = 3
    TASK_STATUS_Y = 2
    TASK_STATUS_G = 1
    TASK_STATUS_ITEMS = (
        (TASK_STATUS_R, 'R'),
        (TASK_STATUS_Y, 'Y'),
        (TASK_STATUS_G, 'G'),
    )

    issue_no = models.CharField(max_length=255, verbose_name="问题代号")
    task_no = models.CharField(max_length=255, verbose_name="任务代号")
    task_content = models.TextField(max_length=1024,  verbose_name="待办事宜")
    follower = models.CharField(max_length=255, verbose_name="跟踪人")
    responsible = models.CharField(max_length=255, verbose_name="责任人")
    raised_date = models.DateField(verbose_name=".__提 出 日 期__." , auto_now=True)
    target_date = models.DateField(verbose_name=".__目 标 日 期__.", auto_now=True)
    closed_date = models.DateField(verbose_name=".__关 闭 日 期__.", auto_now=True)
    # task_status = models.CharField(max_length=50, verbose_name="状态")
    task_status = models.PositiveIntegerField(default=TASK_STATUS_Y, choices=TASK_STATUS_ITEMS, verbose_name="STA")
    task_comments = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    content_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="条目状态")
    is_md = models.BooleanField(default=False, verbose_name="markdown语法")
    task_category = models.ForeignKey(TaskCategory, verbose_name="部    门", on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(TaskTag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="用户", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = "任务"
        ordering = ['-id']

    def __str__(self):
        return self.task_content

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.task_comments)
        else:
            self.content_html = self.task_comments
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = TaskTag.objects.get(id=tag_id)
        except TaskTag.DoesNotExist:
            tag = None
            task_list = []
        else:
            task_list = tag.task_set.filter(status=Task.STATUS_NORMAL)\
                .select_related('owner', 'task_category')
        return task_list, tag

    @staticmethod
    def get_by_category(task_category_id):
        try:
            task_category = TaskCategory.objects.get(id=task_category_id)

        except TaskCategory.DoesNotExist:
            task_category = None
            task_list = []

        else:
            task_list = task_category.task_set.filter(status=Task.STATUS_NORMAL)\
                .select_related('owner', 'task_category')

        return task_list, task_category

    @classmethod
    def latest_tasks(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @classmethod
    def hot_tasks(cls):
        result = cache.get('hot_tasks')
        if not result:
            result = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
            cache.set('hot_tasks', result, 10 * 60)
        return result

    def color_state(self):
        if self.task_status == 3:
            font_code = 'white'
            color_code = '#EE6A50'
            assign_state_name = '未 开 始'

        elif self.task_status == 2:
            font_code = '#EE9572'
            color_code = 'yellow'
            assign_state_name = '进 行 中'
        else:
            font_code = 'white'
            color_code = 'green'
            assign_state_name = '已 完 成'
        return format_html(
            '<span style="color:{}; background:{};font-weight: 520;">{}</span>',
            font_code,
            color_code,
            assign_state_name,
        )

    color_state.short_description = '完成状态'