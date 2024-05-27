from django.test import TestCase
from dot_app.models import Board, Subtype, Manufacturer

BoardPOSTData = {'title': 'TestBoard'}
ManufacturerPOSTData = {'title': 'TestManufacturer'}
SubtypePOSTData = {'name': 'TestSubtype'}
BoardURLTemplate='boards/'
ManufacturerURLTemplate='manufacturers/'
SubtypeURLTemplate='subtypes/'


def create_model_tests(model_cls, attrs):
    class TestModel(TestCase):
        def test_positive_create(self):
            model_cls.objects.create(**attrs)
    return TestModel

BoardModelTest = create_model_tests(Board, BoardPOSTData)
ManufacturerModelTest = create_model_tests(Manufacturer, ManufacturerPOSTData)
SubtypeModelTest = create_model_tests(Subtype, SubtypePOSTData)