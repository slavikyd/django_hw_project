"""Tester of models module."""
from django.contrib.auth.models import User
from django.test import TestCase

import dot_app.models as models

TITLE = 'title'
BOARD = 'board'
SUBTYPE = 'subtype'
MANUF = 'manufacturer'
BoardPOSTData = {TITLE: 'TestBoard'}
ManufacturerPOSTData = {TITLE: 'TestManufacturer'}
SubtypePOSTData = {'name': 'TestSubtype'}
BoardURLTemplate = 'boards/'
ManufacturerURLTemplate = 'manufacturers/'
SubtypeURLTemplate = 'subtypes/'
USER = 'user'


def create_model_tests(model_cls, attrs):
    """Auto-creator of model creation tests.

    Args:
        model_cls (_type_): class of model
        attrs (_type_): attributes for creation

    Returns:
        TestModel: test case for django to handle
    """
    class TestModel(TestCase):
        """Tester of models creation class.

        Args:
            TestCase (_type_): django inheritance
        """

        def test_positive_create(self):
            """Tester for valid creation."""
            model_cls.objects.create(**attrs)

    return TestModel


BoardModelTest = create_model_tests(models.Board, BoardPOSTData)
ManufacturerModelTest = create_model_tests(models.Manufacturer, ManufacturerPOSTData)
SubtypeModelTest = create_model_tests(models.Subtype, SubtypePOSTData)


class TestLinks(TestCase):
    """Tests for links class.

    Args:
        TestCase (_type_): django inheritance to turn class into a test case
    """

    valid_attrs = {
        BOARD: {TITLE: 'Rpi', 'description': 'idk', 'year': 2023},
        SUBTYPE: {'name': 'ABC', 'description': 'ABC'},
        MANUF: {TITLE: 'Rpi inc'},
        'client': {'user': 'testik'},
    }

    def test_boardtype(self):
        """Tester of board-subtype connection."""
        board = models.Board.objects.create(**self.valid_attrs.get(BOARD))
        subtype = models.Subtype.objects.create(**self.valid_attrs.get(SUBTYPE))
        board.subtypes.add(subtype)
        board.save()
        boardsubtype = models.BoardSubtype.objects.filter(board=board, subtype=subtype)
        self.assertEqual(len(boardsubtype), 1)

    def test_boardmanuf(self):
        """Tester of board-manufacturer connection."""
        board = models.Board.objects.create(**self.valid_attrs.get(BOARD))
        manufacturer = models.Manufacturer.objects.create(
            **self.valid_attrs.get(MANUF),
        )
        board.manufacturers.add(manufacturer)
        board.save()
        boardmanufcturer = models.BoardManufacturer.objects.filter(
            board=board, manufacturer=manufacturer,
        )
        self.assertEqual(len(boardmanufcturer), 1)

    def test_boardclient(self):
        """Tester of board-client connection."""
        user = User.objects.create(username=USER, password=USER)
        client = models.Client.objects.create(user=user)
        board = models.Board.objects.create(**self.valid_attrs.get(BOARD))
        client.boards.add(board)
        client.save()
        boardclient = models.BoardClient.objects.filter(board=board, client=client)
        self.assertEqual(len(boardclient), 1)

    def test_str_methods(self):
        """Str methods tester."""
        board = models.Board.objects.create(**self.valid_attrs.get(BOARD))
        manufacturer = models.Manufacturer.objects.create(
            **self.valid_attrs.get(MANUF),
        )
        subtype = models.Subtype.objects.create(**self.valid_attrs.get(SUBTYPE))
        board_attrs = self.valid_attrs[BOARD]
        b_title, b_year = board_attrs[TITLE], board_attrs['year']
        board_str = f'{b_title}, {b_year}, Undefined'
        self.assertEqual(f'{board}', board_str)
        self.assertEqual(f'{manufacturer}', self.valid_attrs[MANUF][TITLE])
        self.assertEqual(f'{subtype}', self.valid_attrs[SUBTYPE]['name'])
