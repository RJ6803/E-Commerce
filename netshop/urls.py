from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('',include('maincore.urls')),
    path('cart/',include('cart.urls')),
    path('order/',include('order.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
