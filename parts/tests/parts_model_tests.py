from django.core.exceptions import ValidationError
from django.test import TestCase

from .parts_view_tests import createPart


class PartModelTest(TestCase):
    def setUp(self) -> None:
        self.part = createPart()
        return super().setUp()

    def test_max_lenght_field_part_name(self):
        self.part.name = 'A' * 26
        with self.assertRaises(ValidationError):
            self.part.full_clean()

    def test_max_lenght_field_cpf_part(self):
        self.part.cpf = 'A' * 55
        with self.assertRaises(ValidationError):
            self.part.full_clean()
