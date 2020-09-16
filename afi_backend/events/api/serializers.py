from rest_framework_json_api import serializers

from afi_backend.events.models import Event, OfflineLecture, Lecturer


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineLecture
        fields = ['address']


class EventSerializer(serializers.ModelSerializer):
    category = EventTypeSerializer(source='content_object', read_only=True)

    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'category',
        ]


class OfflineLectureSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = OfflineLecture
        fields = [
            'name',
            'lecture_date',
            'lecture_date_ts',
            'lecturer',
            'lecture_summary_file',
            'price',
            'price_currency',
        ]


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = [
            'name',
            'userpic',
            'bio',
        ]
