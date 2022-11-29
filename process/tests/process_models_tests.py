from django.core.exceptions import ValidationError
from django.test import TestCase

from .process_adm_views_tests import createProcess


class ProcessModelsTest(TestCase):
    def setUp(self) -> None:
        self.process = createProcess()
        return super().setUp()

    def test_max_lenght_field_number(self):
        self.process.number = 'A' * 26
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_class_process(self):
        self.process.class_process = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_court(self):
        self.process.court = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_forum(self):
        self.process.forum = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_organ(self):
        self.process.organ = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_area(self):
        self.process.area = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_county(self):
        self.process.county = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()

    def test_max_lenght_field_controll(self):
        self.process.controll = 'A' * 55
        with self.assertRaises(ValidationError):
            self.process.full_clean()
