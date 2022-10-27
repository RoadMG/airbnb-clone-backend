from django.contrib import admin
from .models import ChattingRoom, Message


@admin.register(ChattingRoom)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created",
        "updated",
    )
    list_filter = ("created",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "room",
        "created",
    )

    list_filter = ("created",)
