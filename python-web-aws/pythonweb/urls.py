from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('blog/', permanent=False)),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('profile/', include('users.urls')),
]

print(settings.MEDIA_URL)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)