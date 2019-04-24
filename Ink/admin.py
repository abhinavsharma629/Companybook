from django.contrib import admin
from .models import *

#All Tables
admin.site.register(CompOrEmp)
admin.site.register(EmpDate)
admin.site.register(EmpCompany)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(CompanyEmployee)
admin.site.register(EmployementHistory)