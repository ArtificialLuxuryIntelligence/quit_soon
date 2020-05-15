import datetime

from django.test import TransactionTestCase, TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from QuitSoonApp.views import (
    index, today,
    register_view, login_view,
    profile, paquets, alternatives,
    suivi, objectifs,
    new_name, new_email, new_password, new_parameters,
)
from QuitSoonApp.models import (
    UserProfile,
    Paquet, ConsoCig,
    Alternative, ConsoAlternative,
    Objectif, Trophee
)


class RegisterClientTestCase(TestCase):
    """
    Tests on register view
    """

    def setUp(self):
        """setup tests"""
        self.user = User.objects.create_user(
            'registerTestUser', 'test@test.com', 'testpassword')

    def test_get_register_view(self):
        response = self.client.get(reverse('QuitSoonApp:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_succes(self):
        """Test client register with success"""
        data = {'username':'NewUserTest',
                'email':'testnewUser@test.com',
                'password1':'t3stpassword',
                'password2':'t3stpassword'}
        response = self.client.post(reverse('QuitSoonApp:register'),
                                    data=data,
                                    follow=True)
        self.assertRedirects(response, '/today/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertTrue(User.objects.filter(username='NewUserTest').exists())
        self.assertTrue(User.objects.get(username='NewUserTest').is_authenticated)

    def test_register_bad_user(self):
        """Test client register with success"""
        data = {'username':'registerTestUser',
                'email':'testnewUser@test.com',
                'password1':'t3stpassword',
                'password2':'t3stpassword'}
        response = self.client.post(reverse('QuitSoonApp:register'),
                         data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='registerTestUser').exists())
        self.assertFalse(User.objects.get(username='registerTestUser').email == 'testnewUser@test.com')
        self.assertRaises(ValidationError)


    def test_register_bad_email(self):
        """Test client register with success"""
        data = {'username':'NewUserTest',
                'email':'test@test.com',
                'password1':'t3stpassword',
                'password2':'t3stpassword'}
        response = self.client.post(reverse('QuitSoonApp:register'),
                         data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='NewUserTest').exists())
        self.assertRaises(ValidationError)

    def test_register_passwords_diff(self):
        """Test client register with success"""
        data = {'username':'NewUserTest',
                'email':'testnewUser@test.com',
                'password1':'t3stpassword',
                'password2':'t3stdsqfpassword'}
        response = self.client.post(reverse('QuitSoonApp:register'),
                         data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='NewUserTest').exists())
        self.assertRaises(ValidationError)

class LoginClientTestCase(TransactionTestCase):
    """
    Tests on Login view
    """

    def setUp(self):
        """setup tests"""
        self.user = User.objects.create_user(
            'loginTestUser', 'test@test.com', 'testpassword')

    def test_get_login_view(self):
        response = self.client.get(reverse('QuitSoonApp:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')

    def test_login_succes_with_email(self):
        """Test client login with success"""
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')
        data = {'username':'test@test.com',
                'password':'testpassword'}
        response = self.client.post(reverse('QuitSoonApp:login'),
                                    data=data,
                                    follow=True)
        self.assertRedirects(response, '/today/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertTrue(User.objects.filter(username='loginTestUser').exists())
        self.assertTrue(User.objects.get(username='loginTestUser').is_authenticated)
        user = User.objects.get(username='loginTestUser')
        self.assertTrue(auth.get_user(self.client), user)

    def test_login_succes_with_username(self):
        """Test client login with success"""
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')
        data = {'username':'loginTestUser',
                'password':'testpassword'}
        response = self.client.post(reverse('QuitSoonApp:login'),
                                    data=data,
                                    follow=True)
        self.assertRedirects(response, '/today/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertTrue(User.objects.filter(username='loginTestUser').exists())
        self.assertTrue(User.objects.get(username='loginTestUser').is_authenticated)
        user = User.objects.get(username='loginTestUser')
        self.assertTrue(auth.get_user(self.client), user)

    def test_login_wrong_email(self):
        """Test client login failing wrong email"""
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')
        data = {'username':'wrong_email@test.com',
                'password':'testpassword'}
        response = self.client.post(reverse('QuitSoonApp:login'),
                         data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='wrongemail@test.com').exists())
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')
        self.assertRaises(ValidationError)


    def test_login_wrong_password(self):
        """Test client login failing wrong email"""
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')
        data = {'username':'test@test.com',
                'password':'wrongpassword'}
        response = self.client.post(reverse('QuitSoonApp:login'),
                         data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(auth.get_user(self.client), 'AnonymousUser')
        self.assertRaises(ValidationError)


class UserProfileTestCase(TransactionTestCase):
    """Tests on views and features related with user profile"""

    def setUp(self):
        """setup tests"""
        self.user = User.objects.create_user(
            username='Test', email='test@test.com', password='testpassword')

    def test_profile_get_newuser(self):
        self.client.login(username=self.user.username, password='testpassword')
        response = self.client.get(reverse('QuitSoonApp:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'QuitSoonApp/profile.html')
        self.assertEqual(response.context['userprofile'], 'undefined')

    def test_profile_get_anonymoususer(self):
        response = self.client.get(reverse('QuitSoonApp:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'QuitSoonApp/profile.html')
        self.assertEqual(response.context['userprofile'], None)

    def test_profile_get_existing_profile_user(self):
        userprofile = UserProfile.objects.create(
            user=self.user,
            date_start='2012-12-12',
            starting_nb_cig=3
        )
        self.client.login(username=self.user.username, password='testpassword')
        response = self.client.get(reverse('QuitSoonApp:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'QuitSoonApp/profile.html')
        self.assertEqual(response.context['userprofile'], userprofile)

    def test_new_name(self):
        """test change nameview"""
        self.client.login(username=self.user.username, password='testpassword')
        user_id = self.user.id
        data = {'username':'NewName'}
        self.client.post(reverse('QuitSoonApp:new_name'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.filter(username="NewName").exists(), True)
        self.assertEqual(User.objects.filter(username="NewName").count(), 1)
        self.assertEqual(User.objects.get(id=user_id).username, 'NewName')
        self.client.logout()

    def test_new_name_already_in_db(self):
        """test change nameview with integrity error, name already in DB"""
        self.client.login(username=self.user.username, password='testpassword')
        User.objects.create_user(
            username='userinDB', email='Test@…', password='password')
        user_id = self.user.id
        username = self.user.username
        data = {'username':'userinDB'}
        self.client.post(reverse('QuitSoonApp:new_name'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.get(id=user_id).username, username)
        self.assertTrue(User.objects.get(username='userinDB').id != user_id)
        self.client.logout()

    def test_new_email(self):
        """test change nameview"""
        user_id = self.user.id
        self.client.login(username=self.user.username, password='testpassword')
        data = {'email':'New@email.test'}
        self.client.post(reverse('QuitSoonApp:new_email'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.get(id=user_id).email, 'New@email.test')
        self.client.logout()

    def test_new_email_already_in_db(self):
        """test change nameview with integrity error, name already in DB"""
        User.objects.create_user(
            username='userinDB', email='emailalreadyindb@test.com', password='password')
        user_id = self.user.id
        email = self.user.email
        self.client.login(username=self.user.username, password='testpassword')
        data = {'email':'emailalreadyindb@test.com'}
        self.client.post(reverse('QuitSoonApp:new_email'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.get(id=user_id).email, email)
        self.client.logout()

    def test_new_password_success(self):
        """test userpage view in post method"""
        self.client.login(username='Test', password='testpassword')
        data = {
            'old_password': 'testpassword',
            'new_password1': 'mynewpassword',
            'new_password2': 'mynewpassword',
        }
        self.client.post(reverse('QuitSoonApp:new_password'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.get(username="Test").check_password("mynewpassword"), True)
        self.client.logout()

    def test_new_password_fail_no_confirmed(self):
        """test userpage view in post method"""
        self.client.login(username='Test', password='testpassword')
        data = {
            'old_password': 'testpassword',
            'new_password1': 'mynewpassword',
            'new_password2': 'newpassword',
            }
        self.client.post(reverse('QuitSoonApp:new_password'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.get(username="Test").check_password("mynewpassword"), False)
        self.assertEqual(User.objects.get(username="Test").check_password("testpassword"), True)
        self.client.logout()

    def test_new_password_fail_too_short(self):
        """test userpage view in post method"""
        self.client.login(username='Test', password='testpassword')
        data = {
            'old_password': 'testpassword',
            'new_password1': 'secret',
            'new_password2': 'secret',
            }
        self.client.post(reverse('QuitSoonApp:new_password'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.get(username="Test").check_password("secret"), False)
        self.assertEqual(User.objects.get(username="Test").check_password("testpassword"), True)
        self.client.logout()

    def test_new_parameters_get(self):
        response = self.client.post(reverse('QuitSoonApp:new_parameters'))
        self.assertEqual(response.status_code, 200)

    def test_new_parameters_post(self):
        self.client.login(username='Test', password='testpassword')
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())
        data = {
            'date_start': '2020-05-17',
            'starting_nb_cig': 20,
            }
        self.client.post(reverse('QuitSoonApp:new_parameters'),
                         data=data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        self.assertEqual(UserProfile.objects.get(user=self.user).date_start, datetime.date(2020, 5, 17))
        self.assertEqual(UserProfile.objects.get(user=self.user).starting_nb_cig, 20)
