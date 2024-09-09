from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些 Model的 owner字段
    2. 用来针对 queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    def get_queryset(self, request):
        """ 用户只能看到自己创建的文章 """
        qs = super().get_queryset(request)
        # <QuerySet [<Post: Post object (6)>, <Post: Post object (5)>, ...]>
        # 可以取qs.values('id', 'title')
        # print(qs)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user        # 当前已经登录的用户作为作者
        return super().save_model(request, obj, form, change)
