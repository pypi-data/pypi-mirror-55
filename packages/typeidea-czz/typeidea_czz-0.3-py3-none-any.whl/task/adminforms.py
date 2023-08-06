from dal import autocomplete
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms

from .models import TaskCategory, TaskTag, Task


class TaskAdminForm(forms.ModelForm):
    task_content = forms.CharField(widget=forms.Textarea, label='任务内容', required=False)
    task_category = forms.ModelChoiceField(
        queryset=TaskCategory.objects.all(),
        # widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='部门',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=TaskTag.objects.all(),
        # widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    task_status = forms.CharField(widget=forms.TextInput, label='任务状态', required=False)

    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    content = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Task
        # fields = (
        #     'category', 'tag', 'task_comments', 'title',
        #     'is_md', 'task_content', 'content_md', 'content_ck',
        #     'status'
        # )
        fields = (
            'task_category', 'tag', 'task_comments',
            'is_md', 'task_content', 'content_md', 'content_ck',
            'status', 'task_status','responsible','owner'
        )

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.task_content
            else:
                initial['content_ck'] = instance.task_content

        super().__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        task_content = self.cleaned_data.get(content_field_name)
        if not task_content:
            self.add_error(content_field_name, '必填项！')
            return
        self.cleaned_data['task_content'] = task_content
        return super().clean()

    class Media:
        js = ('js/post_editor.js', )
