from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *

#Registration Form
class RegistrationForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','first_name','password1','password2']


#Type of user form
class TypeForm(forms.ModelForm):
	
	#2 Types of users
	TYPE=(
		("employee", ("employee")),
		("company", ("company"))
		)
	typ=forms.ChoiceField(choices=TYPE,required=True)

	class Meta:
		model = CompOrEmp
		fields=['typ']