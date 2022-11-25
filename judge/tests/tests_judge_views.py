# flake8: noqa
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from judge import views
from judge.models import Judge


def login(self):
    user = User.objects.create_user(
        username='user', password='123')
    # Use this:
    return self.client.force_login(user)


def createJudge():
    Judge.objects.create(name='judge', cnj='123')


class JudgeViewsTest(TestCase):

    # test views in the urls

    def test_judge_list_views_function_is_correct(self):
        view = resolve(reverse('judge:list'))
        self.assertIs(view.func.view_class, views.JudgeList)

    def test_judge_register_views_function_is_correct(self):
        view = resolve(reverse('judge:register', kwargs={'path': 'process'}))
        self.assertIs(view.func.view_class, views.JudgeDetails)

    def test_judge_detail_views_function_is_correct(self):
        view = resolve(reverse('judge:detail', kwargs={'id': 1}))
        self.assertIs(view.func.view_class, views.JudgeDetails)

    def test_judge_delete_views_function_is_correct(self):
        view = resolve(reverse('judge:delete', kwargs={'id': 1}))
        self.assertIs(view.func.view_class, views.JudgeDelete)

    # tests status codes views

    def test_judge_list_views_function_is_status_code_200_founded(self):
        login(self)
        response = self.client.get(reverse('judge:list'))
        self.assertEqual(response.status_code, 200)

    def test_judge_register_views_function_is_status_code_200_founded(self):
        login(self)
        response = self.client.get(
            reverse('judge:register', kwargs={'path': ''}))
        self.assertEqual(response.status_code, 200)

    def test_judge_delete_views_function_is_status_code_200_founded(self):
        response = self.client.get(
            reverse('judge:delete', kwargs={'id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    # Exists Judge tests

    def test_status_code_200_ok_in_judge_that_exists(self):
        login(self)
        createJudge()
        response = self.client.get('/Editar/juiz/1/')
        self.assertEqual(response.status_code, 200)

    def test_404_in_jugde_that_no_exists(self):
        # Or this:
       # client.login(username=username, password=password)
        login(self)
        response = self.client.get('/Editar/juiz/1000/')
        self.assertEqual(response.status_code, 404)

    # CHANGE HERE


'''
    def test_judge_list_views_loads_correct_template(self):
        response = self.client.get(
            reverse('judge:detail', kwargs={'id': 2}), follow=True)
        self.assertTemplateUsed(response, 'adm/judge/judgeDetail.html')
'''
# tests templates render
