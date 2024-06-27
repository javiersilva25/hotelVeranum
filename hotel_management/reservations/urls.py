from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('guests/', views.guest_list, name='guest_list'),
    path('guests/new/', views.create_guest, name='create_guest'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/new/', views.create_reservation, name='create_reservation'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/new/', views.create_room, name='create_room'),
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/new/', views.create_promotion, name='create_promotion'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_reservations/', views.user_reservations, name='user_reservations'),
]

