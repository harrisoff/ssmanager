"""ssmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url

from shadowsocks import views as ss_view

shadowsocks_patterns = [
    # ==== API ====
    # ss运行状态
    url(r'^status$', ss_view.status),
    # 增加端口
    url(r'^add/(?P<port>[\d]*)/(?P<pswd>[\w\d_]*)/(?P<auth>[\w\d_]*)$', ss_view.add),
    # 删除端口
    url(r'^del/(?P<port>[\d]*)/(?P<auth>[\w\d_]*)$', ss_view.delete),
    # 列出端口
    url(r'^list$', ss_view.lists),
    # 启动ss
    url(r'^start$', ss_view.start),
    # ==== 页面 ====
    url(r'^admin$', ss_view.page),
]

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^ss/', include(shadowsocks_patterns)),
]
