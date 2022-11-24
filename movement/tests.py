# Create your tests here.
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class MovementUrlsTest(TestCase):

    def test_movement_register_url_is_correct(self):
        url_register = reverse('movement:register', kwargs={'idProcess': 1})
        self.assertEqual(url_register, '/registrarMovimentacao/1/')

    def test_movement_detail_url_is_correct(self):
        url_detail = reverse('movement:detail', kwargs={
                             'id': 1, 'idProcess': 1})
        self.assertEqual(url_detail, '/editar/Movimentacao/1/1/')

    def test_movement_delete_url_is_correct(self):
        url_delete = reverse('movement:delete', kwargs={'id': 1})
        self.assertEqual(url_delete, '/movimentacao/deletar/1/')
