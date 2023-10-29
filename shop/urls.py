from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop import settings
from store.views import index

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', index, name='index'),
        path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
