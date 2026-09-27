from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from monitoramento.views import index


urlpatterns = [

    # Tela de apresentação
    path('', include('monitoramento.urls')),

    path('admin/', admin.site.urls),

    # Página antiga do sistema, preservada
    path('sistema/', index, name='index'),

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