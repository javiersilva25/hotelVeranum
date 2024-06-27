from django.db import models
from django.contrib.auth.models import User

class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.code} - {self.discount_percentage}%'

class Room(models.Model):
    room_number = models.CharField(max_length=5, unique=True)
    room_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    def get_discounted_price(self):
        if self.promotion and self.promotion.start_date <= datetime.date.today() <= self.promotion.end_date:
            discount = self.price_per_night * (self.promotion.discount_percentage / 100)
            return self.price_per_night - discount
        return self.price_per_night

    def __str__(self):
        return f'Room {self.room_number} ({self.room_type})'

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guest')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Reservation for {self.guest} in room {self.room.room_number}'