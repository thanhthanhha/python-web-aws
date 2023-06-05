from . import views
from django.urls import path
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/<str:username>', views.profile, name='users-profile'),
    path('signup', views.signup, name='users-signup'),
    path('signin', views.login_view, name='signin'),
    path('logout', auth_view.LogoutView.as_view(template_name='users/signin.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

