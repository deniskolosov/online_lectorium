
from rest_framework import serializers

from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'name',
            'category',
            'description',
        ]
        filterset_fields = ['category']
        search_fields = ['name']
