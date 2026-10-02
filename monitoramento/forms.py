
from django import forms
from django.contrib.auth.models import User

from .models import (
    Cisterna,
    Dispositivo,
    Municipio,
    PerfilUsuario,
)


PERFIS = [
    ('Administrador do sistema', 'Administrador do sistema'),
    ('Administrador do município', 'Administrador do município'),
    ('Operador-técnico', 'Operador-técnico'),
    ('Visualizador', 'Visualizador'),
]


class CisternaForm(forms.ModelForm):
    class Meta:
        model = Cisterna
        fields = [
            'identificacao',
            'municipio',
            'localidade',
            'participante',
            'latitude',
            'longitude',
            'capacidade_total',
            'situacao',
            'imagem',
        ]
        labels = {
            'identificacao': 'Identificação',
            'municipio': 'Município',
            'localidade': 'Localidade',
            'participante': 'Participante',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'capacidade_total': 'Capacidade total (L)',
            'situacao': 'Situação',
            'imagem': 'Imagem da cisterna',
        }
        widgets = {
            'identificacao': forms.TextInput(
                attrs={'placeholder': 'Ex.: CISTERNA-001'}
            ),
            'latitude': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex.: -5.890000',
                    'step': 'any',
                }
            ),
            'longitude': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex.: -35.270000',
                    'step': 'any',
                }
            ),
            'capacidade_total': forms.NumberInput(
                attrs={'placeholder': 'Ex.: 16000'}
            ),
            'imagem': forms.ClearableFileInput(
                attrs={'accept': 'image/*'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in (
            'identificacao',
            'municipio',
            'localidade',
            'participante',
            'situacao',
        ):
            self.fields[campo].required = True


class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = [
            'identificacao',
            'tipo_sensor',
            'cisterna',
            'data_instalacao',
            'situacao',
        ]
        labels = {
            'identificacao': 'Identificação do dispositivo',
            'tipo_sensor': 'Tipo de sensor',
            'cisterna': 'Cisterna vinculada',
            'data_instalacao': 'Data de instalação',
            'situacao': 'Situação',
        }
        widgets = {
            'identificacao': forms.TextInput(
                attrs={'placeholder': 'Ex.: SENSOR-001'}
            ),
            'tipo_sensor': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: Sensor de nível de água'
                }
            ),
            'cisterna': forms.Select(),
            'data_instalacao': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'situacao': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['identificacao'].required = True
        self.fields['tipo_sensor'].required = True
        self.fields['cisterna'].required = True
        self.fields['data_instalacao'].required = True


class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ['nome', 'estado']
        labels = {
            'nome': 'Nome do município',
            'estado': 'Estado',
        }
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: São Paulo do Potengi'
                }
            ),
            'estado': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: RN',
                    'maxlength': '2',
                }
            ),
        }

    def clean_estado(self):
        return self.cleaned_data['estado'].upper()


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite a senha'}
        ),
    )

    confirmar_senha = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite a senha novamente'}
        ),
    )

    perfil = forms.ChoiceField(
        label='Perfil',
        choices=PERFIS,
    )

    municipio = forms.ModelChoiceField(
        label='Município vinculado',
        queryset=Municipio.objects.all().order_by('nome'),
        required=False,
        empty_label='Selecione um município',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'perfil',
            'municipio',
            'senha',
            'confirmar_senha',
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de usuário',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Nome'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Sobrenome'}
            ),
            'username': forms.TextInput(
                attrs={'placeholder': 'Ex.: joao.silva'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'exemplo@email.com'}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Este nome de usuário já está sendo utilizado.'
            )

        return username

    def clean(self):
        dados = super().clean()

        senha = dados.get('senha')
        confirmar = dados.get('confirmar_senha')

        if senha and confirmar and senha != confirmar:
            self.add_error(
                'confirmar_senha',
                'As senhas não coincidem.',
            )

        if senha and len(senha) < 8:
            self.add_error(
                'senha',
                'A senha deve ter pelo menos 8 caracteres.',
            )

        perfil = dados.get('perfil')
        municipio = dados.get('municipio')

        if (
            perfil in (
                'Administrador do município',
                'Operador-técnico',
                'Visualizador',
            )
            and not municipio
        ):
            self.add_error(
                'municipio',
                'Selecione o município deste usuário.',
            )

        return dados


class UsuarioEdicaoForm(forms.ModelForm):
    perfil = forms.ChoiceField(
        label='Perfil',
        choices=PERFIS,
    )

    municipio = forms.ModelChoiceField(
        label='Município vinculado',
        queryset=Municipio.objects.all().order_by('nome'),
        required=False,
        empty_label='Selecione um município',
    )

    nova_senha = forms.CharField(
        label='Nova senha (opcional)',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': (
                    'Deixe em branco para manter a senha atual'
                )
            }
        ),
    )

    confirmar_senha = forms.CharField(
        label='Confirmar nova senha',
        required=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repita a nova senha'}
        ),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
            'perfil',
            'municipio',
            'nova_senha',
            'confirmar_senha',
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'is_active': 'Usuário ativo',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Nome'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Sobrenome'}
            ),
            'username': forms.TextInput(
                attrs={'placeholder': 'Nome de usuário'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'email@exemplo.com'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            grupo = self.instance.groups.first()

            if grupo:
                nome_perfil = grupo.name

                if nome_perfil == 'Município':
                    nome_perfil = 'Administrador do município'

                if nome_perfil in dict(PERFIS):
                    self.fields['perfil'].initial = nome_perfil

            try:
                perfil_usuario = self.instance.perfil_municipal
                self.fields['municipio'].initial = (
                    perfil_usuario.municipio
                )
            except PerfilUsuario.DoesNotExist:
                pass

    def clean_username(self):
        username = self.cleaned_data['username']

        existentes = User.objects.filter(
            username=username
        ).exclude(pk=self.instance.pk)

        if existentes.exists():
            raise forms.ValidationError(
                'Este nome de usuário já está sendo utilizado.'
            )

        return username

    def clean(self):
        dados = super().clean()

        senha = dados.get('nova_senha')
        confirmar = dados.get('confirmar_senha')

        if senha or confirmar:
            if senha != confirmar:
                self.add_error(
                    'confirmar_senha',
                    'As senhas não coincidem.',
                )
            elif len(senha or '') < 8:
                self.add_error(
                    'nova_senha',
                    'A senha deve ter pelo menos 8 caracteres.',
                )

        # Na edição, o município é opcional.
        # A view pode preservar o município anterior
        # quando nenhum novo município for enviado.

        return dados