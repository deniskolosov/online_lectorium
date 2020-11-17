from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField

from afi_backend.events.models import (Category, Event, Lecturer,
                                       OfflineLecture, VideoLecture,
                                       VideoLectureCertificate,
                                       VideoLectureBulletPoint)
from afi_backend.payments.api.serializers import MembershipField
from afi_backend.exams.api.serializers import TestAssignmentSerializer
from afi_backend.payments.models import Membership


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineLecture
        fields = ['address']


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = [
            'name',
            'userpic',
            'bio',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'color',
        ]


class OfflineLectureSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    included_serializers = {
        'lecturer': LecturerSerializer,
        'category': CategorySerializer
    }

    class Meta:
        model = OfflineLecture
        fields = [
            'name',
            'address',
            'picture',
            'lecture_date',
            'lecture_date_ts',
            'lecturer',
            'category',
            'capacity',
            'description',
            'tickets_sold',
            'lecture_summary_file',
            'price',
            'price_currency',
        ]


class VideoLectureCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLectureCertificate
        fields = [
            'certificate_file',
        ]


class VideoLectureBulletPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLectureBulletPoint
        fields = [
            'text',
        ]


class VideoLectureSerializer(serializers.ModelSerializer):
    tests = TestAssignmentSerializer(many=True, read_only=True)
    included_serializers = {
        'certificate': VideoLectureCertificateSerializer,
        'bullet_points': VideoLectureBulletPointSerializer,
        'lecturer': LecturerSerializer,
        'category': CategorySerializer,
        'allowed_memberships': MembershipField,
    }

    class Meta:
        model = VideoLecture
        fields = [
            'allowed_memberships',
            'bullet_points',
            'category',
            'certificate',
            'description',
            'id',
            'lecturer',
            'vimeo_video_id',
            'name',
            'picture',
            'price',
            'price_currency',
            'tests',
        ]
