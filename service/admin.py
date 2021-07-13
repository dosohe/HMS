from django.contrib import admin

from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    ordering = ('number',)

    list_display = (
        '__str__',
        'number',
        'type',
        'beds',
        'capacity'
    )
