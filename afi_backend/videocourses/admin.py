from import_export import resources
from import_export.admin import ImportExportModelAdmin
from afi_backend.videocourses.models import (CourseLecture, VideoCourse,
                                             VideoCoursePart)
from django.contrib import admin
from afi_backend.videocourses.models import VideoCourseType


class VideoCoursesResource(resources.ModelResource):
    class Meta:
        model = VideoCourse


@admin.register(VideoCourse)
class VideoCourseAdmin(ImportExportModelAdmin):
    resource_class = VideoCoursesResource
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


@admin.register(VideoCourseType)
class VideoCourseTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]
