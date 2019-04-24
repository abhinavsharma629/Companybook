from django.test import TestCase, Client
from .models import *
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.urls import reverse

#Test User creation
class UserTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create(
          username='author12',
          first_name="Author"
        )

        self.publisher = User.objects.create(
          username='publisher@test',
          email='publisher@test.com',
          first_name='Publisher'
        )


    def test_get_authors(self):
    	self.assertEqual(len(User.objects.all()),2)


#Test Registration Form
class TestRegistrationForm(TestCase):
  
  def test_registration_form(self):
    
    # test invalid data
    invalid_data = {
      "username": "user@test.com",
      "first_name": "user",
      "password1": "secret@629",
      "password2": "not secret@629"
    }
    form = RegistrationForm(data=invalid_data)
    form.is_valid()
    self.assertTrue(form.errors)

    # test valid data
    valid_data = {
      "username": "user@test.com",
      "first_name": "user",
      "password1": "secret@629",
      "password2": "secret@629"
    }
    form = RegistrationForm(data=valid_data)
    form.is_valid()
    self.assertFalse(form.errors)


#Testing register Url
class TestUserRegistrationView(TestCase):

  def setUp(self):
    self.client = Client()

  def test_registration(self):
    url = reverse('register')
    
    # test req method GET
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # test req method POST with empty data
    response = self.client.post(url, {})
    self.assertEqual(response.status_code, 200)
    exp_data = {
      'error': True,
      'errors': {
        'username': 'This field is required',
        'password1': 'This field is required',
        'password2': 'This field is required',
      }
    }
    self.assertEqual(response.status_code, 200)
    
    # test req method POST with invalid data
    req_data = {
      'username': 'user@test.com',
      'password1': 'secret@629',
      'password2': 'secret1@629',
    }
    response = self.client.post(url, req_data)
    self.assertEqual(response.status_code, 200)
    exp_data = {
      'error': True,
      'errors': {
        'password2': 'Passwords mismatched'
      }
    }
    self.assertEqual(response.status_code, 200)

    # test req method POST with valid data
    req_data = {
      'username': 'user@test.com',
      'password1': 'secret@629',
      'password2': 'secret@629',
    }
    response = self.client.post(url, req_data)
    
    #302 meaning having additional url in header
    self.assertEqual(response.status_code, 302)
    exp_data = {
      'error': False,
      'message': 'Success, Please login'
    }
    
    #302 meaning having additional url in header
    self.assertEqual(response.status_code, 302)
    self.assertEqual(User.objects.count(), 1)


#Testing type/<Username> Url
class TestUserTypeView(TestCase):

  def setUp(self):
    self.client = Client()
    self.author = User.objects.create(
          username='author12',
          first_name="Author"
        )

  def test_type(self):
    url = reverse('type', kwargs={'username':"author12"})
    
    # test req method GET
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # test req method POST with empty data
    response = self.client.post(url, {})
    self.assertEqual(response.status_code, 200)
    exp_data = {
      'error': True,
      'errors': {
        'typ': 'This field is required',
      }
    }
    self.assertEqual(response.status_code, 200)
    
    # test req method POST with invalid data
    req_data = {
     'typ': 'company',
    }
    response = self.client.post(url, req_data)
    self.assertEqual(response.status_code, 302)
    

    # test req method POST with valid data
    req_data = {
      'typ':'admin',
    }
    response = self.client.post(url, req_data)
    
    #302 meaning having additional url in header
    self.assertEqual(response.status_code, 200)
    self.assertEqual(CompOrEmp.objects.count(), 1)
    self.assertEqual(Company.objects.count(), 1)
    self.assertEqual(Employee.objects.count(), 0)


#Testing ownComp Url
class TestownCompView(TestCase):

	def testOwnHome(TestCase):
		def setUp(self):
			self.client = Client()

		def test_registration(self):
			url = reverse('ownComp')
			# test req method GET
			response = self.client.get(url)
			self.assertEqual(response.status_code, 200)


#Testing join/<companyName> Url
class TestjoinView(TestCase):

	def testjoin(TestCase):
		def setUp(self):
			self.client = Client()

		def test_join(self):
			url = reverse('join', kwargs={'companyName':"author12"})
			response = self.client.get(url)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(EmployementHistory.objects.count(), 1)
			self.assertEqual(CompanyEmployee.objects.count(), 1)
			self.assertEqual(EmpDate.objects.count(), 1)