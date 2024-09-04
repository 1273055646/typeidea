from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Tag, Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')  # 页面上显示的字段
    fields = ('name', 'status', 'is_nav')  # 增加时显示的字段

    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 当前已经登录的用户作为作者
        return super().save_model(request, obj, form, change)

    def post_count(self, obj):
        """ 统计文章数量 """
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']
    list_display_links = []
    list_filter = ['category', ]

    search_fields = ['title', 'category_name']

    actions_on_top = True
    actions_on_bottom = False

    # 编辑页面
    save_on_top = True

    exclude = ('owner',)  # 必须这么写，因为The value of 'exclude' must be a list or tuple.

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        """ 新增编辑按钮 """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=[obj.id])
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
