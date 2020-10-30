from django.contrib import admin
from afi_backend.videocourses.models import VideoCourse, CourseLecture, VideoCoursePart


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
        'part',
    ]
    search_fields = ['name']


@admin.register(VideoCoursePart)
class VideoCoursePartAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]
    search_fields = ['name']
