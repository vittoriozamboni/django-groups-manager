from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin

from testproject import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.TestView.as_view(), name='home'),
    re_path(r'^groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
