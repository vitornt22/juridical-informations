# flake8: noqa
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse, reverse_lazy

from judge.models import Judge
from movement import views
from movement.models import Movement
from process.models import Process


def login(self):
    user = User.objects.create_user(
        username='user', password='123')
    # Use this:
    return self.client.force_login(user)


def createMovement():
    process = createProcess()
    movement = Movement.objects.create(
        date='2022-07-22', description='123', process=process)
    return movement


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


class MovementViewsTest(TestCase):

    # check correct views tests

    def test_movement_register_views_function_is_correct(self):
        login(self)
        createMovement()
        view = resolve(reverse('movement:register',
                       kwargs={'id_process': 1}))
        self.assertIs(view.func.view_class, views.MovementCreateView)

    def test_movement_detail_views_function_is_correct(self):
        login(self)
        createMovement()
        view = resolve(reverse('movement:detail',
                       kwargs={'pk': 1, 'id_process': 1}))
        self.assertIs(view.func.view_class, views.MovementUpdateView)

    def test_movement_delete_views_function_is_correct(self):
        view = resolve(reverse('movement:delete', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.MovementDeleteView)

    # check  status codes  views

    def test_movement_register_views_function_is_status_code_200_founded(self):
        login(self)
        createMovement()
        response = self.client.post(
            reverse('movement:register', kwargs={'id_process': 1}), {'date': "22/07/2022", 'description': "234232", "process": 1}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_movement_delete_views_function_is_status_code_200_founded(self):
        response = self.client.get(
            reverse('movement:delete', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_movement_update_views_function_is_status_code_200_founded(self):
        response = self.client.get(
            reverse('movement:detail', kwargs={'pk': 1, 'id_process': 1}), follow=True)
        self.assertEqual(response.status_code, 200)

    # Exists Movement tests
    def test_status_code_200_ok_in_movement_that_exists(self):
        login(self)
        createMovement()
        response = self.client.get(
            reverse('movement:detail', kwargs={'pk': 1, 'id_process': 1}))
        self.assertEqual(response.status_code, 200)

    def test_404_in_jugde_that_no_exists(self):
        login(self)
        createMovement()
        response = self.client.get(
            reverse('movement:detail', kwargs={'pk': 10000, 'id_process': 1}))
        self.assertEqual(response.status_code, 404)

    # redirects vies tests
    def test_redirect_create_view_register_movement(self):
        login(self)
        createProcess()
        post = self.client.post(
            reverse('movement:register', kwargs={'id_process': 1}),
            {'date': "22/07/2000", 'description': "sskskkks", "process": 1})
        self.assertRedirects(post, reverse(
            'process:detail', kwargs={'pk': 1}))

    def test_redirect_update_view_register_movement(self):
        login(self)
        createMovement()
        post = self.client.post(
            reverse('movement:detail', kwargs={'id_process': 1, 'pk': 1}),
            {'date': "22/07/2003", 'description': "sskskkks", "process": 1})
        self.assertRedirects(post, reverse(
            'process:detail', kwargs={'pk': 1}))

    def test_redirect_delete_view_register_movement(self):
        login(self)
        createMovement()
        post = self.client.post(
            reverse('movement:detail', kwargs={'id_process': 1, 'pk': 1}),
            {'date': "22/07/2003", 'description': "sskskkks", "process": 1})
        self.assertRedirects(post, reverse(
            'process:detail', kwargs={'pk': 1}))

    # templates tests

    def test_template_update_view_register_movement(self):
        login(self)
        createMovement()
        post = self.client.get(
            reverse('movement:detail', kwargs={'id_process': 1, 'pk': 1}))

        self.assertTemplateUsed(post, 'adm/movement/movementDetail.html')
