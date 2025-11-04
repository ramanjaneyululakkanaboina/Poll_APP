from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm

class Questionform(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'category']
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        if Question.objects.filter(question_text__iexact=question_text).exists():
            raise forms.ValidationError("This question already exists!")
        return question_text    

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name', 'description', 'end_time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
