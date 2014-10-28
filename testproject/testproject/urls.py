from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.TestView.as_view(), name='home'),
    url(r'^groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
