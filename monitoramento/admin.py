from django.contrib import admin

from .models import (
    Participante,
    Localidade,
    Cisterna,
    LeituraTelemetria,
    Alerta,
)


admin.site.register(Participante)
admin.site.register(Localidade)
admin.site.register(Cisterna)
admin.site.register(LeituraTelemetria)
admin.site.register(Alerta)