from django.core.exceptions import ValidationError
from django.test import TestCase

from .movement_views_tests import createMovement


class MovementModelsTest(TestCase):
    def setUp(self) -> None:
        self.movement = createMovement()
        return super().setUp()

    def test_max_lenght_field_descriptiion(self):
        self.movement.description = 'A' * 600
        with self.assertRaises(ValidationError):
            self.movement.full_clean()
