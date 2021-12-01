from django.forms import ModelForm, CharField, PasswordInput
from app.models import Carros, Usuarios, Sobre


# Create the form class.
class CarrosForm(ModelForm):
    class Meta:
        model = Carros
        fields = ['modelo', 'marca', 'ano']


class UsuariosForm(ModelForm):
    senha = CharField(widget=PasswordInput())
    class Meta:
        model = Usuarios
        fields = ['email', 'senha']


class SobreForm(ModelForm):
    class Meta:
        model = Sobre
        fields = ['texto']