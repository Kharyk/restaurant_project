
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from project.models import Dish, Table, Comment, Stars, Check, Order, DishPrice, TablePrice
from project.forms import DishForm, TableForm, CommentForm, StarsForm, CheckForm, OrderForm
from datetime import datetime

class UserAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse('dish-list'))

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Test',
            'last_name': 'User ',
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertRedirects(response, reverse('dish-list'))
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertRedirects(response, reverse('home'))


class DishModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.dish = Dish.objects.create(
            name='Test Dish',
            ingredients='Test Ingredients',
            gram='200g',
            sort_daytime='Lunch',
            sort='Main Courses'
        )

    def test_dish_creation(self):
        self.assertEqual(self.dish.name, 'Test Dish')
        self.assertEqual(self.dish.ingredients, 'Test Ingredients')

    def test_dish_list_view(self):
        response = self.client.get(reverse('dish-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Dish')

    def test_dish_detail_view(self):
        response = self.client.get(reverse('dish-detail', kwargs={'pk': self.dish.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Dish')


class TableModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.table = Table.objects.create(
            name='Test Table',
            number_of_people=4,
            zone='Indoors',
            sort='VIP'
        )

    def test_table_creation(self):
        self.assertEqual(self.table.name, 'Test Table')
        self.assertEqual(self.table.number_of_people, 4)

    def test_table_list_view(self):
        response = self.client.get(reverse('table-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Table')

    def test_table_detail_view(self):
        response = self.client.get(reverse('table-detail', kwargs={'pk': self.table.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Table')


class SearchResultsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.dish = Dish.objects.create(
            name='Pasta',
            ingredients='Noodles, Tomato Sauce',
            gram='300g',
            sort_daytime='Lunch',
            sort='Main Courses'
        )
        self.table = Table.objects.create(
            name='Table 1',
            number_of_people=4,
            zone='Indoors',
            sort='VIP'
        )

    def test_search_results_view(self):
        response = self.client.get(reverse('search-results'), {'q': 'Pasta'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta')
        self.assertContains(response, 'Table 1')


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.dish = Dish.objects.create(
            name='Test Dish',
            ingredients='Test Ingredients',
            gram='200g',
            sort_daytime='Lunch',
        )