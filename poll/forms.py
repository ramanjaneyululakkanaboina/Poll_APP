from django import forms
from .models import Question, CustomUser
from django.contrib.auth.forms import UserCreationForm
class Questionform(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']
        