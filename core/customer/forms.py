from django import forms
from django.contrib.auth.models import User
from core.models import Customer, Job
from django.core.exceptions import ValidationError

class UserModifyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class CustomerModifyForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("avatar",)


class JobCreateStep1(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("quantity", "image", "category", "description")
        
        
        
# validation phone_number
def validate_phone_number(value):
    if not value.isdecimal():
        raise ValidationError(
            ('%(value)s is not a valid phone number number'),
            params={'value': value},
        )


class JobCreateStep2(forms.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone = forms.CharField(required=True, validators=[validate_phone_number])

    class Meta:
        model = Job
        fields = ("pickup_address", "pickup_name", "pickup_lat", "pickup_lng", "pickup_phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        self.fields["pickup_lat"].widget = forms.HiddenInput()
        self.fields["pickup_lng"].widget = forms.HiddenInput()
