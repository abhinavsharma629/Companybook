from django.shortcuts import render,redirect
from django.template import loader
from django import forms
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User

#Registeration
def register(request):
	if request.method == "POST":
		try:
			form=RegistrationForm(request.POST)
			# If form Is valid
			if form.is_valid():
				form.save()

				#If Logged In Employee Creating A Company
				if(str(request.user) != "AnonymousUser"):

					#Creating A new Company User
					obj2,notif=User.objects.get_or_create(username=request.POST.get('username'), first_name=request.POST.get('first_name'))
					if notif is True:
						obj.save()

					#Selecting the newly created company
					username=User.objects.get(username=request.POST.get('username'))
					obj,notif=CompOrEmp.objects.get_or_create(name=username, typ="company")
					if notif is True:
						obj.save()

					#Creating A Company Object
					userObj=User.objects.get(username=username)
					obj,notif=Company.objects.get_or_create(company=User.objects.filter(Q(username=username))[0], cmp_id=str(userObj.username))
					if notif is True:
						obj.save()

					#Creating Employee Having A company object
					userObj=User.objects.get(username=username)
					obj1,notif=EmpCompany.objects.get_or_create(emp_id=Employee.objects.get(employee=request.user), cmp_id=obj)
					if notif is True:
						obj1.save()

					return HttpResponseRedirect('/createComp')
				
				else:
					url="/type/"+request.POST.get('username')
					return redirect(url, username=request.POST.get('username'))

		except Exception as e:
			section='/register'
			return HttpResponseRedirect(section)
	
	else:
		form=RegistrationForm()
	args = {"form": form}
	return render(request, 'Ink/register.html', args)


#Register if a newly registered User is a Company or an Employee
def type(request, username):
	if(request.method == "POST"):
		try:
			form=TypeForm(request.POST)
			if form.is_valid():
				obj=form.save(commit=False)

				#Creating Company Or Employee Object to store if the new entry is a company or employee
				obj,notif=CompOrEmp.objects.get_or_create(name=User.objects.filter(Q(username=username))[0], typ=request.POST.get('typ'))
				if notif is True:
					obj.save()

				#Creating Company Object if its a company to store company info.
				if(str(request.POST.get('typ'))=="company"):
					userObj=User.objects.get(username=username)
					obj,notif=Company.objects.get_or_create(company=User.objects.filter(Q(username=username))[0], cmp_id=str(userObj.username))

				#Creating Employee Object if its an employee to store company info.
				elif(str(request.POST.get('typ'))=="employee"):
					userObj=User.objects.get(username=username)
					obj,notif=Employee.objects.get_or_create(employee=User.objects.filter(Q(username=username))[0], emp_id=str(userObj.username))
				
				if notif is True:
					obj.save()
				return HttpResponseRedirect('/createComp')

		except Exception as e:
			url="/type/"+username
			return redirect(url, username=username)
	
	else:
		form=TypeForm()
	args = {"form": form ,'username': username}
	return render(request, 'Ink/type.html', args)


#Home
@login_required(login_url='/')
def home(request):
	try:
		filterUser=CompOrEmp.objects.get(name=request.user)
		
		#If logged in user is a company
		if(filterUser.typ == "company"):
			return HttpResponseRedirect('/company')
		else:
			return HttpResponseRedirect('/employee')	
	except:
		return HttpResponseRedirect('/')


#If logged in is an Employee
@login_required(login_url='/')
def employee(request):
	try:
		#Excluding the self created company of the employee
		comp=Company.objects.all().order_by('-created')
		empComp=Company.objects.exclude(cmp_id__in=[item.cmp_id.cmp_id for item in EmpCompany.objects.all()])
		args={"companies": empComp, 'employee': Employee.objects.get(employee=request.user)}

	except Exception as e:
		return HttpResponseRedirect('/home')
	return render(request, 'Ink/companyList.html', args)


#If employee joins a company
@login_required(login_url='/')
def join(request, companyName):

	cmpObj=Company.objects.filter(Q(cmp_id=companyName))
	empObj=Employee.objects.get(employee=request.user)
	empObj.currentCompany=cmpObj[0]
	try:
		#If he has not joined the company before create a new obj

		if(len(EmployementHistory.objects.all()) ==0 or len(EmpDate.objects.filter(Q(emp_id=empObj), Q(cmp_id=cmpObj[0])))==0):
			
			#Employeement History
			obj, notif=EmployementHistory.objects.get_or_create(emp_id=empObj)
			if(notif==True):
				obj.save()
			obj.companiesAppliedToHistory.add(cmpObj[0])
			obj.save()

			#Tenure of working for each company
			obj, notif=EmpDate.objects.get_or_create(cmp_id=cmpObj[0], emp_id=empObj, created=timezone.now(), left=None)
			if(notif==True):
				obj.save()

			#Which company the employee belongs to
			obj, notif=CompanyEmployee.objects.get_or_create(cmp_id=cmpObj[0])
			if(notif==True):
				obj.save()
			obj.currentEmployees.add(empObj)
			obj.save()

		else:
			#If already worked in the company then update the dates of working
			obj=EmployementHistory.objects.get(emp_id=empObj.emp_id)
			obj.companiesAppliedToHistory.add(cmpObj[0])
			obj.save()
			
			obj=EmpDate.objects.filter(Q(cmp_id=cmpObj[0]),Q(emp_id=empObj))
			for i in obj:
				i.left=None
				i.save()

			obj=CompanyEmployee.objects.get(cmp_id=cmpObj[0])
			obj.currentEmployees.add(empObj)
			obj.save()

	except Exception as e:
		
		obj=EmployementHistory.objects.get(emp_id=empObj.emp_id)
		obj.left=None
		obj.companiesAppliedToHistory.add(cmpObj[0])
		obj.save()

		obj=CompanyEmployee.objects.get(cmp_id=cmpObj[0])
		obj.currentEmployees.add(empObj)
		obj.save()

	empObj.save()
	return HttpResponseRedirect('/home')


#If he leaves the company
@login_required(login_url='/')
def leave(request, companyName):

	cmpObj=Company.objects.filter(Q(cmp_id=companyName))
	empObj=Employee.objects.get(employee=request.user)
	empObj.currentCompany= None
	empObj.save()

	obj=CompanyEmployee.objects.get(cmp_id=cmpObj[0])
	obj.currentEmployees.remove(empObj)
	obj.save()

	obj=EmpDate.objects.filter(Q(cmp_id=cmpObj[0])).order_by('-created')
	for i in obj:
		i.left=timezone.now()
		i.save()
		break

	return HttpResponseRedirect('/home')


#Profile
@login_required(login_url='/')
def profile(request):
	obj=CompOrEmp.objects.get(name=request.user)
	
	# If user is a company
	if(obj.typ=="company"):
		args={'company':obj}
		return render(request, 'Ink/compProfile.html', args)
	else:
		args={'history': EmpDate.objects.filter(Q(emp_id=Employee.objects.get(employee=request.user)))}
		return render(request, 'Ink/profile1.html', args)


#If its a company
@login_required(login_url='/')
def company(request):
	cmpObj=Company.objects.all()
	args={'companies': cmpObj}
	return render(request, 'Ink/compHome.html',args)


#Each company's profile
@login_required(login_url='/')
def compHome(request, cmp_id):
	cmpObj=Company.objects.filter(Q(cmp_id=cmp_id))
	
	args={'employed': EmpDate.objects.filter(Q(cmp_id=cmpObj[0])),
	'currDate': timezone.now()}
	return render(request, 'Ink/company1.html', args)


#Company create page
@login_required(login_url='/')
def createComp(request):
	print(request.user)
	obj=EmpCompany.objects.filter(Q(emp_id=Employee.objects.get(employee=request.user)))
	args={'companies': obj}
	return render(request, 'Ink/createComp.html', args)


#Companies made by employee
@login_required(login_url='/')
def ownComp(request):
	obj=EmpCompany.objects.filter(Q(emp_id=Employee.objects.get(employee=request.user)))
	args={'companies': obj}
	return render(request, 'Ink/ownComp.html', args)