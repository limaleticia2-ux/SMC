from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from monitoramento.views import index


urlpatterns = [
    path('', index, name='index'),

    path('admin/', admin.site.urls),

    path('', include('monitoramento.urls')),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]