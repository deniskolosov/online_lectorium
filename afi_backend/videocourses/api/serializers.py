from rest_framework_json_api import serializers
from afi_backend.videocourses.models import VideoCourse, CourseLecture, VideoCoursePart, VideoCourseType
from afi_backend.events.api import serializers as events_serializers
from afi_backend.payments.api.serializers import MembershipSerializer
from afi_backend.payments.models import Membership
from afi_backend.exams.api.serializers import TestAssignmentSerializer


class CourseLectureSerializer(serializers.ModelSerializer):
    included_serializers = {
        'lecturer': events_serializers.LecturerSerializer,
    }
    part = serializers.CharField(source='part.name')
    part_id = serializers.IntegerField(source='part.id')
    tests = TestAssignmentSerializer(many=True)

    class Meta:
        model = CourseLecture
        fields = [
            'course',
            'description',
            'lecturer',
            'name',
            'part',
            'part_id',
            'vimeo_video_id',
            'tests',
        ]


class VideoCoursePartSerializer(serializers.ModelSerializer):
    tests = TestAssignmentSerializer(many=True)

    class Meta:
        model = VideoCoursePart
        fields = [
            'name',
            'description',
            'course',
            'lectures',
            'tests',
        ]


class VideoCourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCourseType
        fields = [
            'name',
            'description',
        ]


class VideoCourseSerializer(serializers.ModelSerializer):
    is_released = serializers.SerializerMethodField()
    course_parts = serializers.ResourceRelatedField(source='parts',
                                                    many=True,
                                                    read_only=True)
    lectures = serializers.ResourceRelatedField(many=True, read_only=True)
    included_serializers = {
        'lecturer': events_serializers.LecturerSerializer,
        'category': events_serializers.CategorySerializer,
        'course_type': VideoCourseTypeSerializer,
        'lectures': CourseLectureSerializer,
        'allowed_memberships': MembershipSerializer,
        'course_parts': VideoCoursePartSerializer,
    }

    class Meta:
        model = VideoCourse
        fields = [
            'allowed_memberships',
            'category',
            'course_type',
            'course_parts',
            'description',
            'id',
            'is_released',
            'lecturer',
            'lectures',
            'name',
            'parts',
            'price',
            'price_currency',
            'release_date',
        ]

    def get_is_released(self, obj):
        return obj.is_released
