from modeltranslation.translator import register, TranslationOptions
from afi_backend.events.models import OfflineLecture, LectureBase


@register(LectureBase)
class LectureBaseTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(OfflineLecture)
class LectureBaseTranslationOptions(TranslationOptions):
    fields = (
        'address',
    )
