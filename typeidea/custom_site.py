from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Typeidea'         # 定义admin站点顶部导航栏中显示的标题
    site_title = 'Typeidea 管理后台'   # 定义了admin站点页面的<title>标签和页面头部（通常是在<h1>标签中）显示的标题。
    index_title = '首页'              # 定义了admin站点索引页面（即通常所说的“首页”）上显示的标题


custom_site = CustomSite(name='cus_admin')
