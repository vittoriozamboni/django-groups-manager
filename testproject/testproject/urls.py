import django
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from testproject import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.TestView.as_view(), name='home'),
    url(r'^groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
