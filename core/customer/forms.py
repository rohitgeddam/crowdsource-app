from django import forms
from django.contrib.auth.models import  User
from core.models import Customer, Job

class UserModifyForm(forms.ModelForm):

    class Meta:
        model=User
        fields = ("first_name", "last_name")

class CustomerModifyForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields = ("avatar",)

class JobCreateStep1(forms.ModelForm):
    
    class Meta:
        model=Job
        fields = ('description', 'quantity', 'image', 'category')