from django import forms
from .models import Register,Edit_Details,project_desc
from django.contrib.auth.forms import AuthenticationForm
class Postform(forms.ModelForm):
    class Meta:
        model=Register
        widgets = {
            'c_password': forms.PasswordInput(),
            'c_confirm_password' : forms.PasswordInput(),
        }
        fields=['c_name','c_professor_name','c_password','c_contact','c_email','c_details']
class Loginform(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    def clean(self):
        pass

class EditForm(forms.ModelForm):
    class Meta :
        model = Register
        fields=['c_details','c_email','c_ppt']

class projectReqs(forms.ModelForm):
    class Meta:
        model = project_desc
        widgets = {
            'date_expiry': forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'}),
            'date_published': forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'}),
        }
        fields=['c_position','c_description','c_stipend_offered','c_branch','c_course','date_published','date_expiry']

class ChangePass(forms.ModelForm):
    class Meta:
        fields=['c_oldpassword','c_newpassword','c_confirm_password']
