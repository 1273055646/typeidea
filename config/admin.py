from django.contrib import admin

from .models import Link, SideBar
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 当前已经登录的用户作为作者
        return super().save_model(request, obj, form, change)


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
