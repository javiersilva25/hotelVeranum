from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Guest, Reservation, Room
from .forms import GuestForm, ReservationForm, RoomForm, SignUpForm

def index(request):
    return render(request, 'reservations/index.html')

@login_required
@permission_required('reservations.add_guest', raise_exception=True)
def create_guest(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guest created successfully.')
            return redirect('guest_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = GuestForm()
    return render(request, 'reservations/guest_form.html', {'form': form})

@login_required
@permission_required('reservations.view_guest', raise_exception=True)
def guest_list(request):
    guests = Guest.objects.all()
    return render(request, 'reservations/guest_list.html', {'guests': guests})

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            if not hasattr(request.user, 'guest'):
                messages.error(request, 'You need to create a guest profile first.')
                return redirect('create_guest')
            reservation.guest = request.user.guest  # Asignar el usuario actual como invitado
            room_id = request.POST.get('room')  # Obtener el ID de la habitación seleccionada
            reservation.room = get_object_or_404(Room, id=room_id)  # Asignar la habitación correcta
            reservation.save()
            messages.success(request, 'Reservation created successfully.')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation_form.html', {'form': form})

@login_required
@permission_required('reservations.view_reservation', raise_exception=True)
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

@login_required
def user_reservations(request):
    reservations = Reservation.objects.filter(guest=request.user.guest)
    return render(request, 'reservations/user_reservations.html', {'reservations': reservations})

@login_required
@permission_required('reservations.add_room', raise_exception=True)
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully.')
            return redirect('room_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = RoomForm()
    return render(request, 'reservations/room_form.html', {'form': form})

@login_required
@permission_required('reservations.view_room', raise_exception=True)
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'reservations/room_list.html', {'rooms': rooms})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear un Guest asociado al User
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
            messages.success(request, 'Registration successful.')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
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
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_dashboard(request):
    rooms = Room.objects.filter(available=True)
    return render(request, 'reservations/user_dashboard.html', {'rooms': rooms})
