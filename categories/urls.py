from . import views
from django.urls import path


urlpatterns = [
    path(
        "",
        views.categories,
    ),
    path(
        "<int:pk>",
        views.category,
    ),
]
