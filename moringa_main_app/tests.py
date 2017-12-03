from django.test import TestCase
from moringa_main_app.models import Students, GlobalAdmin, LocalAdmin, Attendance
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class SignUpViewsTest(TestCase):
    
    def test_correct_view(self):
        # get view by url
        resp = self.client.get('/signup/')
        self.assertEqual(resp.status_code, 200)

        # get view by name
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)

        # check correct template
        resp = self.client.get(reverse('signup'))
        self.assertTemplateUsed(resp, 'registration/signup.html')
    
    # incomplete, dunno how to test a form
    def test_valid_student_sign_up(self):
        # TO DO sign up as a student
        # redirect to login
        self.assertRedirects(resp, '/login/')

    def test_valid_local_admin_sign_up(self):
        # TO DO sign up as a local admin
        # redirect to login
        self.assertRedirects(resp, '/login/')

    def test_valid_global_admin_sign_up(self):
        # TO DO sign up as a global admin
        # redirect to login
        self.assertRedirects(resp, '/login/')

class LoginViewsTest(TestCase):

    def setUp(self):
        #Create one user
        test_user1 = User.objects.create_user(username='testuser1', password='12345') 
        test_user1.save()
    
    def test_correct_view(self):
        # get view by url
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

        # get view by name
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

        # check correct template
        resp = self.client.get(reverse('login'))
        self.assertTemplateUsed(resp, 'registration/login.html')
    
    # incomplete, not sure how login is differentiating student/LA/GA
    # change setup to create 3 separate test users: 1 student, 1 LA, 1 GA
    def test_valid_student_user_login(self):
        resp = self.client.login(username='testuser1', password='12345')
        self.assertRedirects(resp, '/check_in/')

    def test_valid_local_admin_user_login(self):
        resp = self.client.login(username='testuser1', password='12345')
        self.assertRedirects(resp, '/local_admin/')
    
    def test_valid_global_admin_user_login(self):
        resp = self.client.login(username='testuser1', password='12345')
        self.assertRedirects(resp, '/global_admin/')

    def test_invalid_user_login(self):
        resp = self.client.login(username='fakeuser', password='phony')

        # check that redirects to login page
        self.assertRedirects(resp, '/login/')
        # check that response outputs an error message
        self.assertContains(resp, 'Wrong username and password combination')

class LogoutViewTest(TestCase):
    
    def setUp(self):
        #Create one user
        test_user1 = User.objects.create_user(username='testuser1', password='12345') 
        test_user1.save()
        # login user
        self.client.login(username='testuser1', password='12345')

    def test_correct_logout_view(self):
        # get view by url
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 200)

        # get view by name
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 200)

        # check correct template
        resp = self.client.get(reverse('logout'))
        self.assertTemplateUsed(resp, 'registration/login.html')

class StudentsCheckInViewsTest(TestCase):

    def setUp(self):
        #Create one user
        test_user1 = User.objects.create_user(username='testuser1', password='12345') 
        test_user1.save()
    
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('check_in'))
        self.assertRedirects(resp, '/login/')
    
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('check_in'))
        
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'student_view/check_in.html')

    def test_check_in_input_excuse(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.post(reverse('check_in'), {'excuse': 'this is a test excuse'})

        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Check that we redirect to "view_record" page
        self.assertRedirects(resp, '/view_record/')

        #Check we used correct template in redirect
        self.assertTemplateUsed(resp, 'student_view/view_record.html')
    
    # add tests for users in different scenarios (absent, tardy, present)


