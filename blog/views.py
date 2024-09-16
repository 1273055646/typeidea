from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from config.models import SideBar
from .models import Post, Category, Tag


# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#             'category': category,
#             'tag': tag,
#             'post_list': post_list,
#             'sidebars': SideBar.objects.all(),
#         }
#
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.objects.all(),
#     }
#
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
#
#
# class PostListView(ListView):
#     queryset = Post.latest_posts()
#     paginate_by = 2
#     context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用 object_list 变量
#     template_name = 'blog/list.html'


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.objects.all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')

        category = get_object_or_404(Category, id=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset, 根据标签过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, id=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset, 根据标签过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
