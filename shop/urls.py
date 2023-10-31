from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import signup, logout_user, login_user
from shop import settings
#from store import views
from store.views import index, product_detail, add_to_cart, cart, delete_cart

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', index, name='index'),
        path('signup/', signup, name='signup'),
        path('login/', login_user, name='login'),
        path('logout/', logout_user, name='logout'),
        path('cart/', cart, name='cart'),
        path('cart/delete/', delete_cart, name='delete-cart'),
        path('shoe/<str:slug>/', product_detail, name='shoe'),
        path('shoe/<str:slug>/add-to-cart/', add_to_cart, name='add-to-cart'),
        path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

