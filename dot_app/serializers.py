from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Board, Manufacturer, Subtype, Client

class BoardSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = [
            'id', 'title', 'description',
            'type', 'year',
            'created', 'modified',
        ]

class ManufacturerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class SubtypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subtype
        fields = '__all__'