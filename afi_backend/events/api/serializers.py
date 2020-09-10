
from ..models import Event, OfflineLecture
from rest_framework_json_api import relations, serializers, filters, django_filters
from rest_framework.filters import SearchFilter


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
