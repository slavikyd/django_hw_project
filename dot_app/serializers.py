"""Serializers for django project rest implementation."""
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Board, Manufacturer, Subtype


class BoardSerializer(HyperlinkedModelSerializer):
    """Serializer for board models.

    Args:
        HyperlinkedModelSerializer (_type_): django rest inheritance
    """

    class Meta:
        """Settings subclass."""

        model = Board
        fields = [
            'id',
            'title',
            'description',
            'type',
            'year',
            'created',
            'modified',
        ]


class ManufacturerSerializer(HyperlinkedModelSerializer):
    """Serializer for manufacturer models.

    Args:
        HyperlinkedModelSerializer (_type_): django rest inheritance
    """

    class Meta:
        """Settings subclass."""

        model = Manufacturer
        fields = '__all__'


class SubtypeSerializer(HyperlinkedModelSerializer):
    """Serializer for subtype models.

    Args:
        HyperlinkedModelSerializer (_type_): django rest inheritance
    """

    class Meta:
        """Settings subclass."""

        model = Subtype
        fields = '__all__'
