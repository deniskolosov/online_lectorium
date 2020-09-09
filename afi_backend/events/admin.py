from django.contrib import admin
from .models import Event, Lecturer, OfflineLecture

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'event_type']
    search_fields = ['id']



@admin.register(OfflineLecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']



@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['name']
