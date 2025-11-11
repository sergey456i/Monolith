from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Question, Choice

class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'short_description', 'full_description', 'image', 'lifetime_hours']
        labels = {
            'title' : 'Название',
            'short_description' : 'Краткое описание ',
            'full_description' : 'Полное описание',
            'image' : 'Фото',
            'lifetime_hours' : 'Время жизни опроса'
                 }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']