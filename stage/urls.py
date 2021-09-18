from django.urls import path,include 
from . import views
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.welcome, name='welcome'),
    path('signup/', views.usersignup, name='signup'),
    path('activate/<uidb64>/<token>/',
        views.activate_account, name='activate'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.PasswordsChangeView.as_view(), name='password_change'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
