from modeltranslation.translator import register, TranslationOptions
from afi_backend.videocourses.models import VideoCourse, CourseLecture


@register(VideoCourse)
class VideoCourseTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(CourseLecture)
class CourseLectureTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )
