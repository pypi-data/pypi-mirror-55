from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed


from .models import Task


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestTaskFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = "Task Management System"
    link = "/rss/"
    description = "Sync system power by czz"

    def items(self):
        return Task.objects.filter(status=Task.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.task_comments

    def item_link(self, item):
        return reverse('task-detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html
