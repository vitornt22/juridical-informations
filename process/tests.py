from django.test import TestCase
from django.urls import reverse


class ProcessUrlsTest(TestCase):
    def test_the_pytest_is_ok(self):
        assert 1 == 1

    def test_process_home_url_is_correct(self):
        url_home = reverse('process:home')
        self.assertEqual(url_home, '/home')

    def test_process_login_url_is_correct(self):
        url_login_page = reverse('process:loginPage')
        self.assertEqual(url_login_page, '/')

    def test_process_logout_url_is_correct(self):
        url_logout_page = reverse('process:logout')
        self.assertEqual(url_logout_page, '/Logout')

    def test_process_details_client_url_is_correct(self):
        url_detail_clients = reverse('process:detailClient', kwargs={'id': 1})
        self.assertEqual(url_detail_clients, '/detalhes/processo/1')

    def test_process_search_client_url_is_correct(self):
        url_detail_clients = reverse('process:searchProcess')
        self.assertEqual(url_detail_clients, '/pequisarProcessos/')

    def test_process_list_url_is_correct(self):
        url_list = reverse('process:list')
        self.assertEqual(url_list, '/processos')

    def test_process_export_csv_url_is_correct(self):
        url_export_csv = reverse('process:export')
        self.assertEqual(url_export_csv, '/export')

    def test_process_register_url_is_correct(self):
        url_register = reverse('process:register')
        self.assertEqual(url_register, '/registrar/processo/')

    def test_process_detail_url_is_correct(self):
        url_detail = reverse('process:detail', kwargs={'id': 1})
        self.assertEqual(url_detail, '/editar/processo/1/')

    def test_process_delete_url_is_correct(self):
        url_delete = reverse('process:delete', kwargs={'id': 1})
        self.assertEqual(url_delete, '/deletar/Processo/1/')

    def test_process_shut_down_url_is_correct(self):
        url_shut_down = reverse('process:shutdown', kwargs={
                                'id': 1, 'idPart': 1})
        self.assertEqual(url_shut_down, '/desligarParte/1/1')
