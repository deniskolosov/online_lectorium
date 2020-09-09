
from rest_framework import serializers

from ..models import Event, OfflineLecture



class OfflineLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineLecture
        fields = ['address', 'description']

class CategoryEventField(serializers.RelatedField):
    """
    Field to use for representing generic relationship to Event Categories,
    """

    def to_representation(self, value):
        """
        Serialize Event Categories to text
        """
        if isinstance(value, OfflineLecture):
            serializer = OfflineLectureSerializer(value)
        # add more checks here
        # elif isinstance(value, )
        else:
            raise Exception("Unexpected type of Event")
        return serializer.data


class EventSerializer(serializers.ModelSerializer):
    category = CategoryEventField(source='content_object', read_only=True)

    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'category',
        ]
        filterset_fields = ['category']
        search_fields = ['name']
