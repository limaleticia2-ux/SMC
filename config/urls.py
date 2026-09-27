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

    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(
            template_name='monitoramento/recuperacao_senha/form.html'
        ),
        name='recuperar_senha'
    ),

    path(
        'recuperar-senha/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='monitoramento/recuperacao_senha/enviado.html'
        ),
        name='recuperar_senha_enviado'
    ),

    path(
        'recuperar-senha/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='monitoramento/recuperacao_senha/nova_senha.html'
        ),
        name='recuperar_senha_confirmar'
    ),

    path(
        'recuperar-senha/concluido/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='monitoramento/recuperacao_senha/concluido.html'
        ),
        name='recuperar_senha_concluido'
    ),
]