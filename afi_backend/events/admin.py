from django.contrib import admin

from afi_backend.events.models import (
    VideoLecture,
    VideoLectureBulletPoint,
    VideoLectureCertificate,
)

from afi_backend.events.models import (Category, Event, Lecturer,
                                       LectureRating, OfflineLecture,
                                       UsersVideoLectureCertificates)


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
    ]


class LectureRatingAdmin(LectureRating):
    pass


class BulletPointsInline(admin.StackedInline):
    model = VideoLectureBulletPoint


@admin.register(VideoLecture)
class VideoLectureAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'vimeo_video_id',
    ]
    inlines = [BulletPointsInline]


@admin.register(VideoLectureCertificate)
class VideoLectureCertificateAdmin(admin.ModelAdmin):
    list_display = [
        'certificate_file',
    ]


@admin.register(VideoLectureBulletPoint)
class VideoLectureBulletPointAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'video_lecture',
    ]


@admin.register(UsersVideoLectureCertificates)
class UsersVideoLectureCertificatesAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'certificate',
    ]
