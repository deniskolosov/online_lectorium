
from modeltranslation.translator import register, TranslationOptions
from afi_backend.blog.models import Post


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        'content',
    )
