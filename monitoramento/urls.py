from django.urls import path

from .views import landing, painel


urlpatterns = [
    path('', landing, name='landing'),
    path('painel/', painel, name='painel'),
]