from modeltranslation.translator import register, TranslationOptions
from afi_backend.events.models import OfflineLecture, LectureBase, VideoLecture, VideoLectureBulletPoint


@register(LectureBase)
class LectureBaseTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


@register(OfflineLecture)
class OfflineLectureTranslationOptions(TranslationOptions):
    fields = ('address', )


@register(VideoLecture)
class VideoLectureTranslationOptions(TranslationOptions):
    pass


@register(VideoLectureBulletPoint)
class VideoLectureBulletPointTranslationOptions(TranslationOptions):
    fields = ('text', )
