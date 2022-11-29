from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class JudgeUrlsTest(TestCase):

    def test_the_pytest_is_ok(self):
        assert 1 == 1

    def test_judge_list_url_is_correct(self):
        url_list = reverse('judge:list')
        self.assertEqual(url_list, '/juizes/')

    def test_judge_register_url_is_correct(self):
        url_register = reverse('judge:RegisterJudge')
        self.assertEqual(url_register, '/juiz/registrarJuiz')

    def test_judge_detail_url_is_correct(self):
        url_detail = reverse('judge:detail', kwargs={'pk': 1})
        self.assertEqual(url_detail, '/juiz/Editar/1/')

    def test_judge_delete_url_is_correct(self):
        url_delete = reverse('judge:delete', kwargs={'pk': 1})
        self.assertEqual(url_delete, '/juiz/deletar/1/')
