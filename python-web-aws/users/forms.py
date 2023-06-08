from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from .models import Profile
from blog.models import Post

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        template_name = 'user/profile_image.html'
        model = Profile
        fields = ['image','short_bio','long_bio']

class PasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class PostFormUpdate(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']

class PostFormCreate(forms.ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Post
        fields = ['title','content','image']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True, author=None):
        post = super().save(commit=False)
        if author:
            post.author = author
        if commit:
            post.save()
        return post