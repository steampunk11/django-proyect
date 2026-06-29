# vamos a crar el formulario registro nuevo para el sistema
# esto es ua funcionalidad de django
""" importa el formulacion creacional  que django nos ofrece para crear un nuevo usuario y el modelo de usuario que es el que se va a utilizar para crear el nuevo usuario en la base de datos """
from django.contrib.auth.forms import UserCreationForm
# importamos el modelo de usuario que es el que se va a utilizar para crear el nuevo usuario en la base de datos
from django.contrib.auth.models import User # type: ignore 
# importamis el modulo del formulario de django para crear un nuevo formulario de registro de usuario
from django import forms # type: ignore
# impoertamos el modulo personalizado record
from .models import Record # type: ignore

# formulario  de registro  personalidado  badado en el formulario de creacion de usuario de django UserCreationForm.
class SignUpForm(UserCreationForm):
    # Definimos campos adicionales si los necesitas, por ejemplo el email
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        # Lista de campos que se mostrarán en el formulario de registro
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        # Aplicamos clases de Bootstrap a todos los campos automáticamente
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].help_text = "" # Limpia textos de ayuda largos de Django

        # Personalización del mensaje de verificación para password2
        if 'password2' in self.fields:
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingrese la misma contraseña que antes, para verificación.</small></span>'

class AddRecordForm(forms.ModelForm):
    # Este es el otro formulario que mencionaba tu log de error
    class Meta:
        from .models import Record
        model = Record
        fields = "__all__" # O lista los campos: ['first_name', 'last_name', etc.]
        
    def __init__(self, *args, **kwargs):
        super(AddRecordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})