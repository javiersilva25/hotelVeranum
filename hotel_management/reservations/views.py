from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Guest, Reservation, Room, Promotion
from .forms import GuestForm, ReservationForm, RoomForm, SignUpForm, PromotionForm

def index(request):
    """
    Renderiza la página de inicio.
    """
    return render(request, 'reservations/index.html')

@login_required
@permission_required('reservations.add_guest', raise_exception=True)
def create_guest(request):
    """
    Maneja la creación de un nuevo huésped.
    Solo accesible por usuarios con permisos de administrador.
    """
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Huésped creado con éxito.'))
            return redirect('guest_list')
        else:
            messages.error(request, _('Por favor, corrige el error a continuación.'))
    else:
        form = GuestForm()
    return render(request, 'reservations/guest_form.html', {'form': form})

@login_required
@permission_required('reservations.view_guest', raise_exception=True)
def guest_list(request):
    """
    Muestra una lista de todos los huéspedes.
    Solo accesible por usuarios con permisos de administrador.
    """
    guests = Guest.objects.all()
    return render(request, 'reservations/guest_list.html', {'guests': guests})

@login_required
@permission_required('reservations.view_reservation', raise_exception=True)
def reservation_list(request):
    """
    Muestra una lista de todas las reservas.
    Solo accesible por usuarios con permisos de administrador.
    """
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

@login_required
@permission_required('reservations.add_room', raise_exception=True)
def create_room(request):
    """
    Maneja la creación de una nueva habitación.
    Solo accesible por usuarios con permisos de administrador.
    """
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Habitación creada con éxito.'))
            return redirect('room_list')
        else:
            messages.error(request, _('Por favor, corrige el error a continuación.'))
    else:
        form = RoomForm()
    return render(request, 'reservations/room_form.html', {'form': form})

@login_required
@permission_required('reservations.view_room', raise_exception=True)
def room_list(request):
    """
    Muestra una lista de todas las habitaciones.
    Solo accesible por usuarios con permisos de administrador.
    """
    rooms = Room.objects.all()
    return render(request, 'reservations/room_list.html', {'rooms': rooms})

@login_required
def create_reservation(request):
    """
    Maneja la creación de una nueva reserva.
    Asigna el usuario actual como el huésped asociado a la reserva.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            if not hasattr(request.user, 'guest'):
                messages.error(request, _('Primero necesitas crear un perfil de huésped.'))
                return redirect('create_guest')
            reservation.guest = request.user.guest  # Asignar el usuario actual como invitado
            room_id = request.POST.get('room')  # Obtener el ID de la habitación seleccionada
            reservation.room = get_object_or_404(Room, id=room_id)  # Asignar la habitación correcta
            reservation.save()
            messages.success(request, _('Reserva creada con éxito.'))
            return redirect('user_dashboard')
        else:
            messages.error(request, _('Por favor, corrige el error a continuación.'))
    else:
        promotions = Promotion.objects.filter(start_date__lte=date.today(), end_date__gte=date.today())
        form = ReservationForm()
        form.fields['promotion'].queryset = promotions
    return render(request, 'reservations/reservation_form.html', {'form': form})

@login_required
def user_reservations(request):
    """
    Muestra una lista de reservas del usuario actual.
    """
    reservations = Reservation.objects.filter(guest=request.user.guest)
    return render(request, 'reservations/user_reservations.html', {'reservations': reservations})

@login_required
@permission_required('reservations.add_promotion', raise_exception=True)
def create_promotion(request):
    """
    Maneja la creación de una nueva promoción.
    Solo accesible por usuarios con permisos de administrador.
    """
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promoción creada con éxito.')
            return redirect('promotion_list')
        else:
            messages.error(request, 'Por favor, corrige el error a continuación.')
    else:
        form = PromotionForm()
    return render(request, 'reservations/promotion_form.html', {'form': form})

@login_required
@permission_required('reservations.view_promotion', raise_exception=True)
def promotion_list(request):
    """
    Muestra una lista de todas las promociones.
    Solo accesible por usuarios con permisos de administrador.
    """
    promotions = Promotion.objects.all()
    return render(request, 'reservations/promotion_list.html', {'promotions': promotions})

def signup(request):
    """
    Maneja el registro de nuevos usuarios y la creación del perfil de huésped asociado.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Guest.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address')
            )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, _('Registro exitoso.'))
            return redirect('user_dashboard')
        else:
            messages.error(request, _('Por favor, corrige el error a continuación.'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    """
    Maneja la autenticación de usuarios.
    Redirige al tablero de usuario o a la página de inicio dependiendo del rol del usuario.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('index')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, _('Nombre de usuario o contraseña inválidos.'))
        else:
            messages.error(request, _('Por favor, corrige el error a continuación.'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_dashboard(request):
    """
    Muestra el tablero de usuario con una lista de habitaciones disponibles.
    """
    rooms = Room.objects.filter(available=True)
    promotions = Promotion.objects.filter(start_date__lte=date.today(), end_date__gte=date.today())
    today = date.today()
    return render(request, 'reservations/user_dashboard.html', {'rooms': rooms, 'promotions': promotions, 'today': today})
