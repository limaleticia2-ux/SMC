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


class LeituraTelemetria(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="leituras"
    )

    nivel = models.FloatField()

    data_hora = models.DateTimeField()

    def __str__(self):
        return f"{self.cisterna} - {self.data_hora}"


class Alerta(models.Model):
    cisterna = models.ForeignKey(
        Cisterna,
        on_delete=models.CASCADE,
        related_name="alertas"
    )

    mensagem = models.CharField(max_length=255)

    data_hora = models.DateTimeField()

    def __str__(self):
        return self.mensagem