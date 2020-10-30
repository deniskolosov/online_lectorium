from rest_framework_json_api import serializers
from afi_backend.videocourses.models import VideoCourse, CourseLecture
from afi_backend.events.api import serializers as events_serializers
from afi_backend.payments.api.serializers import MembershipSerializer
from afi_backend.payments.models import Membership


class CourseLectureSerializer(serializers.ModelSerializer):
    included_serializers = {
        'lecturer': events_serializers.LecturerSerializer,
    }
    part = serializers.CharField(source='part.name')

    def __init__(self, *args, **kwargs):
        # Exclude video_link, lecture_test fields for nonauthenticated users
        super().__init__(self, *args, **kwargs)
        user = self.context['request'].user
        if user.is_anonymous or user.user_membership.membership.membership_type == Membership.TIER.FREE:
            self.fields.pop('video_link')
            self.fields.pop('lecture_test')

    class Meta:
        model = CourseLecture
        fields = [
            'name',
            'description',
            'course',
            'part',
            'lecturer',
            'video_link',
            'lecture_test',
        ]


class VideoCourseSerializer(serializers.ModelSerializer):
    is_released = serializers.SerializerMethodField()
    included_serializers = {
        'lecturer': events_serializers.LecturerSerializer,
        'category': events_serializers.CategorySerializer,
        'lectures': CourseLectureSerializer,
        'allowed_memberships': MembershipSerializer
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
            'allowed_memberships',
            'lectures',
        ]

    def get_is_released(self, obj):
        return obj.is_released
