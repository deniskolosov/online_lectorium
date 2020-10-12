from rest_framework_json_api import serializers
from afi_backend.videocourses.models import VideoCourse, CourseLecture
from afi_backend.events.api import serializers as events_serializers


class CourseLectureSerializer(serializers.ModelSerializer):
    included_serializers = {
        'lecturer': events_serializers.LecturerSerializer,
    }

    class Meta:
        model = CourseLecture
        fields = [
            'name',
            'description',
            'course',
            'lecturer',
            'video_link',
            'lecture_test',
        ]


class VideoCourseSerializer(serializers.ModelSerializer):
    is_released = serializers.SerializerMethodField()
    included_serializers = {
        'lecturer': events_serializers.LecturerSerializer,
        'category': events_serializers.CategorySerializer,
        'lectures': CourseLectureSerializer
    }

    class Meta:
        model = VideoCourse
        fields = [
            'id',
            'name',
            'description',
            'lecturer',
            'release_date',
            'is_released',
            'category',
            'price',
            'price_currency',
            'lectures',
        ]

    def get_is_released(self, obj):
        return obj.is_released
