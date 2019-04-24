from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
import uuid

#Type of user
class CompOrEmp(models.Model):
	
	#2 Types of users
	TYPE=(
		("employee", ("employee")),
		("company", ("company"))
		)
	name=models.ForeignKey(User, on_delete=models.CASCADE)
	typ=models.CharField(max_length=50, choices=TYPE)


#Company Details with user obj as a foreign key linking user account with user details
class Company(models.Model):
	company=models.ForeignKey(User, on_delete=models.CASCADE)
	cmp_id=models.CharField(max_length=1000,primary_key=True)
	image=models.ImageField(upload_to='pictures', blank=True)
	created=models.DateTimeField(auto_now=True)


#Employee Details with user obj as a foreign key linking user account with user details
class Employee(models.Model):
	employee=models.ForeignKey(User, on_delete=models.CASCADE)
	emp_id=models.CharField(max_length=1000,primary_key=True)
	image=models.ImageField(upload_to='pictures', blank=True)
	currentCompany= models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)


#Current employees of a company with employee as a many to many relation
class CompanyEmployee(models.Model):
	cmp_id=models.ForeignKey(Company, on_delete=models.CASCADE)
	currentEmployees= models.ManyToManyField(Employee)


#Employement history of an employee with company as a many to many relation
class EmployementHistory(models.Model):
	emp_id=models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
	companiesAppliedToHistory= models.ManyToManyField(Company)
	

'''Employement tenure in a company details with repetition allowed for the case if user
worked and then left and then joined again'''
class EmpDate(models.Model):
	id1 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	cmp_id=models.ForeignKey(Company, on_delete=models.CASCADE)
	emp_id=models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
	created=models.DateTimeField()
	left=models.DateTimeField(null=True, blank=True)


#Employee creating his own company having the emp_id and cmp_id as the foreign keys
class EmpCompany(models.Model):
	emp_id=models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
	cmp_id=models.ForeignKey(Company, on_delete=models.CASCADE)