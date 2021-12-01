from django.forms import ModelForm
from app.models import Carros, Usuarios


# Create the form class.
class CarrosForm(ModelForm):
    class Meta:
        model = Carros
        fields = ['modelo', 'marca', 'ano']


class UsuariosForm(ModelForm):
    class Meta:
        model = Usuarios
        fields = ['email', 'senha']