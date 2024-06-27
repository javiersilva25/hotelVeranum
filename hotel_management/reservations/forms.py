from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Guest, Reservation, Room, Promotion

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
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'phone_number': 'Número de Teléfono',
            'address': 'Dirección',
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date', 'promotion']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'promotion': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'room': 'Habitación',
            'check_in_date': 'Fecha de Entrada',
            'check_out_date': 'Fecha de Salida',
            'promotion': 'Promoción',
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
            'room_number': 'Número de Habitación',
            'room_type': 'Tipo de Habitación',
            'description': 'Descripción',
            'price_per_night': 'Precio por Noche',
            'available': 'Disponible',
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Obligatorio. Introduce una dirección de correo válida.', widget=forms.EmailInput(attrs={'class': 'form-control'}))
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
            'username': 'Nombre de Usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone_number': 'Número de Teléfono',
            'address': 'Dirección',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['code', 'description', 'discount_percentage', 'start_date', 'end_date']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'code': 'Código',
            'description': 'Descripción',
            'discount_percentage': 'Porcentaje de Descuento',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin',
        }