from django.db import models


class Participante(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    nome = models.CharField(max_length=150)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.estado}"


class Localidade(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Cisterna(models.Model):
    SITUACAO_CHOICES = [
        ('normal', 'Normal'),
        ('atencao', 'Atenção'),
        ('critico', 'Crítico'),
        ('sem_dados', 'Sem dados'),
    ]

    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name="cisternas"
    )

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name="cisternas",
        null=True,
        blank=True
    )

    localidade = models.ForeignKey(
        Localidade,
        on_delete=models.CASCADE,
        related_name="cisternas"
    )

    identificacao = models.CharField(max_length=100)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    capacidade_total = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    situacao = models.CharField(
        max_length=20,
        choices=SITUACAO_CHOICES,
        default='sem_dados'
    )

    imagem = models.ImageField(
        upload_to='cisternas/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.identificacao


class Dispositivo(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('manutencao', 'Em manutenção'),
    ]

    identificacao = models.CharField(
        max_length=100,
        unique=True
    )

    tipo_sensor = models.CharField(
        max_length=100
    )

    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="dispositivos"
    )

    data_instalacao = models.DateField()

    situacao = models.CharField(
        max_length=20,
        choices=SITUACAO_CHOICES,
        default='ativo'
    )

    def __str__(self):
        return self.identificacao


class LeituraTelemetria(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="leituras"
    )

    dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete=models.SET_NULL,
        related_name="leituras",
        null=True,
        blank=True
    )

    nivel = models.FloatField()

    data_hora = models.DateTimeField()

    def __str__(self):
        return f"{self.cisterna} - {self.data_hora}"

    def save(self, *args, **kwargs):

        nova_leitura = self.pk is None

        super().save(*args, **kwargs)

        if self.nivel >= 70:
            nova_situacao = 'normal'

        elif self.nivel >= 30:
            nova_situacao = 'atencao'

        else:
            nova_situacao = 'critico'

        self.cisterna.situacao = nova_situacao

        self.cisterna.save(
            update_fields=['situacao']
        )

        if nova_leitura and self.nivel < 30:

            leitura_anterior = (
                LeituraTelemetria.objects
                .filter(
                    cisterna=self.cisterna
                )
                .exclude(
                    pk=self.pk
                )
                .order_by(
                    '-data_hora'
                )
                .first()
            )

            if (
                leitura_anterior is None
                or leitura_anterior.nivel >= 30
            ):

                alerta = Alerta.objects.create(
                    cisterna=self.cisterna,
                    mensagem=(
                        f"Nível crítico de água: "
                        f"{self.nivel:.1f}%."
                    ),
                    data_hora=self.data_hora
                )

                from .notificacoes import enviar_email_alerta

                enviar_email_alerta(alerta)


class Alerta(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="alertas"
    )

    mensagem = models.CharField(
        max_length=255
    )

    data_hora = models.DateTimeField()

    def __str__(self):
        return self.mensagem