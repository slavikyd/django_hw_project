from django.test import TestCase
from dot_app.models import Board, Subtype, Manufacturer
import data
def create_model_tests(model_cls, attrs):
    class TestModel(TestCase):
        def test_positive_create(self):
            model_cls.objects.create(**attrs)
    return TestModel

BoardModelTest = create_model_tests(Board, data.BoardPOSTData)
ManufacturerModelTest = create_model_tests(Manufacturer, data.ManufacturerPOSTData)
SubtypeModelTest = create_model_tests(Subtype, data.SubtypePOSTData)