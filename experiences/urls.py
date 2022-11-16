from django.urls import path
from . import views

urlpatterns = [
    path("perks/", views.Perks.as_view()),
    path("perks/<int:perks_pk>", views.PerkDetail.as_view()),
    path("", views.Experiecnes.as_view()),
    path("<int:pk>", views.ExperiencesDetail.as_view()),
    path("<int:pk>/perks", views.ExperiencePerks.as_view()),
    path("<int:pk>/bookings", views.ExperienceBooking.as_view()),
    path("<int:pk>/bookings/<int:booking_pk>", views.ExperienceBookingDetail.as_view()),
]
