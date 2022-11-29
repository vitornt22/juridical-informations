# flake8: noqa
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from judge.models import Judge
from process import views
from process.models import Process


def login(self):
    user = User.objects.create_user(
        username='user', password='123')
    # Use this:
    return self.client.force_login(user)


def createProcess():
    judge = Judge.objects.create(name='judge', cnj='23324')
    process = Process.objects.create(
        number="334329", class_process="criminal",
        forum="Forum 1", subject="objective",
        organ="organ", area="area",
        county="county", controll="control",
        distribution="distribution", judge=judge,
        value=500, status=True,
    )
    return process


class ProcessViewsTest(TestCase):

    # test views in the urls
    def test_process_list_views_function_is_correct(self):
        view = resolve(reverse('process:list'))
        self.assertIs(view.func.view_class, views.ProcessList)

    def test_process_register_views_function_is_correct(self):
        view = resolve(reverse('process:register'))
        self.assertIs(view.func.view_class, views.ProcessCreateView)

    def test_process_detail_views_function_is_correct(self):
        view = resolve(reverse('process:detail', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.ProcessUpdateView)

    def test_process_delete_views_function_is_correct(self):
        view = resolve(reverse('process:delete', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.ProcessDeleteView)

    # tests status codes views
    def test_process_list_views_function_is_status_code_200_founded(self):
        login(self)
        response = self.client.get(reverse('process:list'))
        self.assertEqual(response.status_code, 200)

    def test_process_register_views_function_is_status_code_200_founded(self):
        response = self.client.post(
            reverse('process:register'), {'name': "teste123", 'cpf': "234232"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_process_detail_views_function_is_status_code_200_founded(self):
        login(self)
        createProcess()
        response = self.client.post(
            reverse('process:detail', kwargs={'pk': 1}), {'name': "teste123", 'cpf': "234232"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_process_delete_views_function_is_status_code_200_founded(self):
        response = self.client.get(
            reverse('process:delete', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    # Exists Process tests

    def test_status_code_200_ok_in_process_that_exists(self):
        login(self)
        createProcess()
        response = self.client.get(reverse('process:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_404_in_jugde_that_no_exists(self):
        login(self)
        response = self.client.get(
            reverse('process:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_status_code_200_ok_delete_process_that_exists(self):
        login(self)
        createProcess()
        response = self.client.get(
            reverse('process:delete', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_404_delete_process_that_no_exists(self):
        login(self)
        response = self.client.get(
            reverse('process:delete', kwargs={'pk': 1000000}))
        self.assertEqual(response.status_code, 404)

    # templates and rediredts tests

    def test_template_create_view_register_process(self):
        login(self)
        post = self.client.post(
            reverse('process:register'), {'name': "teste123", 'cpf': "234232"}, follow=True)
        self.assertTemplateUsed(post, 'adm/process/processRegister.html')

    def test_template_detail_view_register_process_in_process_register_page(self):
        login(self)
        createProcess()
        post = self.client.post(
            reverse('process:detail', kwargs={'pk': 1}), {'name': "teste123", 'cpf': "234232"}, follow=True)
        self.assertTemplateUsed(post, 'adm/process/processDetail.html')

    def test_template_list_view_register_process_in_process_register_page(self):
        login(self)
        createProcess()
        response = self.client.get(
            reverse('process:list'), follow=True)
        self.assertTemplateUsed(response, 'adm/process/processList.html')

    def test_redirect_delete_view_register_process_in_process_register_page(self):
        login(self)
        createProcess()
        response = self.client.get(
            reverse('process:delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(response, reverse('process:list'))
