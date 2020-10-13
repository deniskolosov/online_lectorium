from django.contrib import admin
from afi_backend.videocourses.models import VideoCourse, CourseLecture


@admin.register(VideoCourse)
class VideoCourseAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'release_date',
    ]
    search_fields = ['name']


@admin.register(CourseLecture)
class CourseLectureAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'course',
    ]
    search_fields = ['name']
