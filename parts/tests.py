from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class PartUrlsTest(TestCase):
    def test_the_pytest_is_ok(self):
        assert 1 == 1

    def test_part_list_url_is_correct(self):
        url_list = reverse('part:list')
        self.assertEqual(url_list, '/partes/')

    def test_part_register_url_is_correct(self):
        url_register = reverse('part:register', kwargs={'path': 'processo'})
        self.assertEqual(url_register, '/processo/novaParte/')

    def test_part_detail_url_is_correct(self):
        url_detail = reverse('part:detail', kwargs={'id': 1})
        self.assertEqual(url_detail, '/editarParte/1/')

    def test_part_detail_part_process_url_is_correct(self):
        url_detail = reverse('part:detailPartProcess',
                             kwargs={'id': 1, 'idP': 1})
        self.assertEqual(url_detail, '/editarParte/1/1/')

    def test_part_delete_url_is_correct(self):
        url_delete = reverse('part:delete', kwargs={'id': 1})
        self.assertEqual(url_delete, '/deletar/1/')
