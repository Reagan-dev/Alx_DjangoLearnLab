from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

def clean_email(self):
	email = self.cleaned_data.get('email')
	if User.objects.filter(email__iexact=email).exists():
		raise forms.ValidationError("A user with that email already exists.")
	return email


class ProfileForm(forms.Form):
	email = forms.EmailField(required=True)
	bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
	

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
		
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']