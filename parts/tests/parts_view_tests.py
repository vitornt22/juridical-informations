# flake8: noqa
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from judge.models import Judge
from parts import views
from parts.models import Part
from process.models import Process


def login(self):
    user = User.objects.create_user(
        username='user', password='123')
    # Use this:
    return self.client.force_login(user)


def createPart():
    part = Part.objects.create(name='parts')
    return part


def createProcess():
    judge = Judge.objects.create(name='judge')
    process = Process.objects.create(
        number="334329", class_process="criminal",
        forum="Forum 1", subject="objective",
        organ="organ", area="area",
        county="county", controll="control",
        distribution="distribution", judge=judge,
        value=500, status=True,
    )
    return process


class PartViewsTest(TestCase):

    # test views in the urls
    def test_parts_list_views_function_is_correct(self):
        view = resolve(reverse('part:list'))
        self.assertIs(view.func.view_class, views.PartListView)

    def test_parts_register_views_function_is_correct(self):
        view = resolve(reverse('part:register'))
        self.assertIs(view.func.view_class, views.PartCreateView)

    def test_parts_register_in_process_page_views_function_is_correct(self):
        view = resolve(reverse('part:processPartRegister'))
        self.assertIs(view.func.view_class, views.PartCreateView)

    def test_parts_detail_views_function_is_correct(self):
        view = resolve(reverse('part:detail', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.PartUpdateView)

    def test_parts_delete_views_function_is_correct(self):
        view = resolve(reverse('part:delete', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.PartDeleteView)

    # tests status codes views
    def test_parts_list_views_function_is_status_code_200_founded(self):
        login(self)
        response = self.client.get(reverse('part:list'))
        self.assertEqual(response.status_code, 200)

    def test_parts_register_views_function_is_status_code_200_founded(self):
        response = self.client.post(
            reverse('part:register'), {'name': "teste123"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_parts_register_views_in_process_register_page_function_is_status_code_200_founded(self):
        response = self.client.post(
            reverse('part:processPartRegister'), {'name': "teste123"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_parts_delete_views_function_is_status_code_200_founded(self):
        response = self.client.get(
            reverse('part:delete', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create_view_parts_in_register_process_page_status_code(self):
        post = self.client.post(
            reverse('part:processPartRegister'), {'name': "teste123"}, follow=True)
        self.assertEqual(post.status_code, 200)

    # Exists Part tests

    def test_status_code_200_ok_in_parts_that_exists(self):
        login(self)
        createPart()
        response = self.client.get(reverse('part:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_404_in_jugde_that_no_exists(self):
        login(self)
        response = self.client.get(reverse('part:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    # create view redirects

    def test_redirect_create_view_register_parts(self):
        login(self)
        post = self.client.post(
            reverse('part:register'), {'name': "teste123"}, follow=True)
        self.assertRedirects(post, reverse('part:list'))

    def test_redirect_create_view_register_parts_in_process_register_page(self):
        login(self)
        post = self.client.post(
            reverse('part:processPartRegister'), {'name': "teste123"}, follow=True)
        self.assertRedirects(post, reverse('process:register'))
