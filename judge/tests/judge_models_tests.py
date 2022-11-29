from django.core.exceptions import ValidationError
from django.test import TestCase

from .tests_judge_views import createJudge


class JudgeModelsTest(TestCase):
    def setUp(self) -> None:
        self.judge = createJudge()
        return super().setUp()

    def test_max_lenght_field_name_judge(self):
        self.judge.name = 'A' * 150
        with self.assertRaises(ValidationError):
            self.judge.full_clean()

    def test_max_lenght_field_cnj(self):
        self.judge.cnj = 'A' * 55
        with self.assertRaises(ValidationError):
            self.judge.full_clean()
