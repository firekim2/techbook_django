"""techbooks2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^health_check/$', views.health_check, name='health_check'),
    url(r'^techbook/$', views.download_page, name='download_page'),
    url(r'^techbook/version_info/$', views.version, name='version'),
    url(r'^techbook/notice/$', views.notice, name='notice'),
    url(r'^techbook/login/$', views.app_login, name='app_login'),
    url(r'^techbook/edition_info/$', views.edition_info, name='edition_info'),
    url(r'^techbook/article/$', views.article, name='article'),
    url(r'^techbook/message/$', views.message, name='message'),
    url(r'^techbook/calender_info/$', views.calender_info, name='calender_info'),
    url(r'^techbook/youtube/(?P<video_address>.*)/$', views.youtube, name='youtube'),
    url(r'^techbook/admin/$', views.admin_login, name='admin_login'),
    url(r'^techbook/admin/main/$', views.admin_main, name='admin_main'),
    url(r'^techbook/admin/version/$', views.admin_version, name='admin_version'),
    url(r'^techbook/admin/message/$', views.admin_message, name='admin_message'),
    url(r'^techbook/admin/notice/$', views.admin_notice, name='admin_notice'),
    url(r'^techbook/admin/edition/new/$', views.admin_edition_new, name='admin_edition_new'),
    url(r'^techbook/admin/edition/(?P<edition_number>.*)/$', views.admin_edition_modify, name='admin_edition_modify'),
    url(r'^techbook/admin/webviewer/(?P<edition_number>.*)/$', views.admin_webviewer, name='admin_webviewer'),
    url(r'^techbook/admin/article/new/$', views.admin_article_new, name='admin_article_new'),
    url(r'^techbook/admin/article/image_upload/$', views.image_upload, name='image_upload'),
    url(r'^techbook/admin/article/(?P<address>.*)/$', views.admin_article_modify, name='admin_article_modify'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
