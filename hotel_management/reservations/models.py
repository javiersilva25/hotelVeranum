from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_number = models.CharField(max_length=5, unique=True)
    room_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'Room {self.room_number} ({self.room_type})'

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guest')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f'Reservation for {self.guest} in room {self.room.room_number}'

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        constraints = [
            models.UniqueConstraint(fields=['room', 'check_in_date'], name='unique_room_reservation')
        ]
