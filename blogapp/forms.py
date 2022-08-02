from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm
from django.contrib.auth.models import User
from blogapp.models import Profile, Post, Comment, SubComment

from django.contrib.auth import authenticate

# -------------------------------------------------

class SignUpForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}),min_length=4, max_length=10)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control x1','placeholder':'Email'}))  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='Password Confirmation')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control x5','placeholder':'last name'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is not unique")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email

    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise forms.ValidationError("Password don't match")  
        return password2  

# ----------------------------------------

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}))  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

# --------------------------------------

class UserPasswordReset(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

# --------------------------------------

class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x1','placeholder':'Old Password'}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'New Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password does not match")
        return old_password

# ------------------------------------

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','bio','instagram','facebook','twitter']
        labels = {'image':'Image'}
        widgets = {
            'profile_image':forms.FileInput(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class':'form-control x4','placeholder':'Bio', 'rows':4, 'cols':15}),
            'instagram':forms.URLInput(attrs={'class':'form-control x4','placeholder':'Instagram'}),
            'facebook':forms.URLInput(attrs={'class':'form-control x4','placeholder':'Facebook'}),
            'twitter':forms.URLInput(attrs={'class':'form-control x4','placeholder':'Twitter'})
        }

# ---------------------------------------

class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'},
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'first_name':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'email':forms.TextInput(attrs={'class':'form-control x5','placeholder':'email'}),
        }

class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','category','image']
        labels = {'title':'Title','content':'Content','category':'Category','image':'Image'}
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title','maxlength':'200'}),
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Content'}),
            'category':forms.Select(attrs={'class':'form-select'}),
            'image':forms.FileInput(attrs={'class':'form-control'})
        }


