from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Task


class TaskSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Task.objects.filter(status=Task.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('task-detail', args=[obj.pk])
