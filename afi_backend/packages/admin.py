from django.contrib import admin
from afi_backend.packages.models import VideoCoursePackage, VideoLecturePackage


@admin.register(VideoCoursePackage)
class VideoCoursePackageAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoLecturePackage)
class VideoLecturePackageAdmin(admin.ModelAdmin):
    pass
