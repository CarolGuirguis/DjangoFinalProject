from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Categories,Posts,ForbiddenWords,Comment,Reply,Tag


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    is_staff=forms.BooleanField(required=False)
  
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','is_staff')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class CategoryForm(forms.ModelForm):
 
    class Meta:
        model = Categories
        fields = '__all__'
        exclude = ['users']
      
    def clean(self):
        pass

class PostForm(forms.ModelForm):
 
    class Meta:
        model = Posts
        fields = '__all__'
        exclude=['likes','dislikes']
      
    def clean(self):
        pass

class ForbiddenWordForm(forms.ModelForm):
 
    class Meta:
        model = ForbiddenWords
        fields = '__all__'
      
    def clean(self):
        pass

class CommentForm(forms.ModelForm):
 
    class Meta:
        model = Comment
        fields = ['content']
      
    def clean(self):
        pass

class ReplyForm(forms.ModelForm):
 
    class Meta:
        model = Reply
        fields = ['content']
      
    def clean(self):
        pass

class TagForm(forms.ModelForm):
    
 
    class Meta:
        model = Tag
        fields = '__all__'
        labels = {
            "tagword": "Tag",
            
        }
      
    def clean(self):
        pass