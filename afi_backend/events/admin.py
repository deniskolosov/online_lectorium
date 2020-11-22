from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from afi_backend.events.models import (Category, Event, Lecturer,
                                       LectureRating, OfflineLecture,
                                       UsersVideoLectureCertificates,
                                       VideoLecture, VideoLectureBulletPoint,
                                       VideoLectureCertificate)
from afi_backend.videocourses.models import VideoCourse
from afi_backend.packages.models import VideoCoursePackage, VideoLecturePackage


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


# Import Resources https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-import-export-resource
class VideoLectureResource(resources.ModelResource):
    class LecturerWidget(ForeignKeyWidget):
        def clean(self, value, row):
            return self.model.objects.get(name__iexact=row["lecturer"], )

    class CategoryWidget(ForeignKeyWidget):
        def clean(self, value, row):
            return self.model.objects.get(name__iexact=row["category"], )

    lecturer = fields.Field(column_name='lecturer',
                            attribute='lecturer',
                            widget=LecturerWidget(Lecturer, 'name'))
    category = fields.Field(column_name='category',
                            attribute='category',
                            widget=CategoryWidget(Category, 'name'))

    certificate = fields.Field(column_name='certificate_id',
                               attribute='certificate',
                               widget=ForeignKeyWidget(VideoLectureCertificate,
                                                       'id'))

    class Meta:
        model = VideoLecture
        import_id_fields = ('name', )
        fields = (
            'id',
            'name',
            'picture',
            'description',
            'lecturer',
            'lecture_summary_file',
            'price_currency',
            'price',
            'category',
            'vimeo_video_id',
            'certificate',
        )

        exclude = (
            'lecturebase_ptr',
            'allowed_memberships',
            'rating',
        )


@admin.register(VideoLecture)
class VideoLectureAdmin(ImportExportModelAdmin):
    resource_class = VideoLectureResource
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
