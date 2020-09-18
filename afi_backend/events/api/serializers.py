from rest_framework_json_api import serializers

from afi_backend.events.models import Event, OfflineLecture, Lecturer, Category


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
