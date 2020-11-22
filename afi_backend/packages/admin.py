from django.contrib import admin
from afi_backend.packages.models import VideoCoursePackage, VideoLecturePackage
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class VideoCoursePackageResource(resources.ModelResource):
    class Meta:
        model = VideoCoursePackage


class VideoLecturePackageResource(resources.ModelResource):
    class Meta:
        model = VideoLecturePackage


@admin.register(VideoCoursePackage)
class VideoCoursePackageAdmin(ImportExportModelAdmin):
    resource_class = VideoCoursePackageResource


@admin.register(VideoLecturePackage)
class VideoLecturePackageAdmin(admin.ModelAdmin):
    resource_class = VideoLecturePackageResource
