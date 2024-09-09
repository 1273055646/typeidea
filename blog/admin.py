from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from blog.models import Tag, Category, Post
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):
    # 在分类的增加页面中可以对文章进行编辑
    fields = ('title', 'desc')  # 定义了在内联表单中要显示的字段（对文章中的标题和摘要进行编辑）
    extra = 1   # 控制额外多几个
    model = Post   # 与Post关联


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline]  # 这个属性是一个列表，包含了要在Category编辑页面上显示的内联模型类。
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')  # 页面上显示的字段
    fields = ('name', 'status', 'is_nav')  # 增加时显示的字段

    def post_count(self, obj):
        """ 统计文章数量 """
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        # print(Category.objects.filter(owner=request.user).values_list('id', 'name'))
        # <QuerySet [(5, 'wdq'), (6, 'wwww')]>
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        # print(self.value())
        # 6          (显示id)
        category_id = self.value()
        if category_id:
            return queryset.filter(category__id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  # 显示摘要改为Textarea组件
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']
    list_display_links = []
    list_filter = [CategoryOwnerFilter]

    search_fields = ['title', 'category_name']

    actions_on_top = True
    actions_on_bottom = False

    # 编辑页面
    save_on_top = True

    exclude = ('owner',)  # 必须这么写，因为The value of 'exclude' must be a list or tuple.

    """
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    上面和下面两种方法效果类似, 变动的地方都是在新增页面中显示，下面信息更全

    """

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',  # 这实际上不是Django admin标准fieldsets的一部分，但可以用作注释
            'fields': (
                ('title', 'category'),  # 这是一个字段对，通常用于将两个字段显示在同一行
                'status',  # 这是另一个字段，默认会单独显示在一行
            ),
        }),
        ('内容', {
            'fields': (
                'desc',  # 字段名，单独显示在一行
                'content',  # 另一个字段名，也单独显示在一行
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),  # 这是一个元组，包含一个CSS类名，用于折叠该部分
            'fields': (
                'tag',  # 字段名，单独显示在一行（在折叠部分）
            ),
        }),
    )
    # filter_horizontal = ('tag', )  # 横向展示
    filter_vertical = ('tag',)  # 纵向展示

    def operator(self, obj):
        """ 新增编辑按钮 """
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=[obj.id])
        )

    operator.short_description = '操作'
