
from django import forms
from models import UserModel, PostModel, LikeModel, CommentModel
from django .contrib import messages
from django.core.exceptions import ValidationError

#class for sinup form
class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']                   #form fields

    def clean_username(self):
        name = self.cleaned_data['username']
        if name == None:
            raise ValidationError("Username cannot be empty")
        return name

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == None:
            raise ValidationError("name cannot be empty")
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


#class for login form
class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


#class for post form
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']


#class for like form
class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields=['post']

#class for comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post','id']


#class for upvote form
class UpvoteForm(forms.Form):
    id = forms.IntegerField()






