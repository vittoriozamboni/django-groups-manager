import django
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from testproject import views

if django.VERSION >= (1, 9, 0):
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    ]
else:
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
    ]


urlpatterns += [
    url(r'^$', views.TestView.as_view(), name='home'),
    url(r'^groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
