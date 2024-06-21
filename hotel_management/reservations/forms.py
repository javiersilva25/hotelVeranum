from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .models import Guest, Reservation, Room

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'email': _('Correo Electrónico'),
            'phone_number': _('Número de Teléfono'),
            'address': _('Dirección'),
        }
        help_texts = {
            'first_name': _('Introduce tu nombre'),
            'last_name': _('Introduce tu apellido'),
            'email': _('Introduce tu correo electrónico'),
            'phone_number': _('Introduce tu número de teléfono'),
            'address': _('Introduce tu dirección'),
        }
        error_messages = {
            'first_name': {
                'required': _('Este campo es obligatorio.'),
            },
            'last_name': {
                'required': _('Este campo es obligatorio.'),
            },
            'email': {
                'required': _('Este campo es obligatorio.'),
                'invalid': _('Introduce una dirección de correo electrónico válida.'),
            },
            'phone_number': {
                'required': _('Este campo es obligatorio.'),
            },
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'room': _('Habitación'),
            'check_in_date': _('Fecha de Entrada'),
            'check_out_date': _('Fecha de Salida'),
        }
        error_messages = {
            'room': {
                'required': _('Este campo es obligatorio.'),
            },
            'check_in_date': {
                'required': _('Este campo es obligatorio.'),
            },
            'check_out_date': {
                'required': _('Este campo es obligatorio.'),
            },
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'description', 'price_per_night', 'available']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'room_number': _('Número de Habitación'),
            'room_type': _('Tipo de Habitación'),
            'description': _('Descripción'),
            'price_per_night': _('Precio por Noche'),
            'available': _('Disponible'),
        }
        error_messages = {
            'room_number': {
                'required': _('Este campo es obligatorio.'),
            },
            'room_type': {
                'required': _('Este campo es obligatorio.'),
            },
            'price_per_night': {
                'required': _('Este campo es obligatorio.'),
                'invalid': _('Introduce un precio válido.'),
            },
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_('Obligatorio. Introduce una dirección de correo válida.'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': _('Nombre de Usuario'),
            'password1': _('Contraseña'),
            'password2': _('Confirmar Contraseña'),
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'phone_number': _('Número de Teléfono'),
            'address': _('Dirección'),
        }
        help_texts = {
            'username': _('Obligatorio. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ únicamente.'),
            'password1': _('Tu contraseña debe tener al menos 8 caracteres.'),
            'password2': _('Introduce la misma contraseña para verificación.'),
        }
        error_messages = {
            'username': {
                'required': _('Este campo es obligatorio.'),
            },
            'password1': {
                'required': _('Este campo es obligatorio.'),
                'invalid': _('Introduce una contraseña válida.'),
            },
            'password2': {
                'required': _('Este campo es obligatorio.'),
                'invalid': _('Las contraseñas no coinciden.'),
            },
            'first_name': {
                'required': _('Este campo es obligatorio.'),
            },
            'last_name': {
                'required': _('Este campo es obligatorio.'),
            },
            'email': {
                'required': _('Este campo es obligatorio.'),
                'invalid': _('Introduce una dirección de correo electrónico válida.'),
            },
            'phone_number': {
                'required': _('Este campo es obligatorio.'),
            },
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Contraseña"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
