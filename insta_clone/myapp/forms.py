from django import forms
from models import UserModel, PostModel, LikeModel, CommentModel
from django .contrib import messages
#class for sinup form

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']   #form fields

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

#class for sinup form
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']