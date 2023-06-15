from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

from testproject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TestView.as_view(), name='home'),
    path('groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
