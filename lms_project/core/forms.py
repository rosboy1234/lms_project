from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Submission

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'role':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission 
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5,
                'placeholder': "Введіть вашу відповідь або посилання на виконану роботу..."
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ""

class GradingForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': "Напишіть коментар до роботи..."
            }),
            'grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Оцінка (0-100)",
                'min': 0,
                'max': 100
            })
        }
        labels = {
            'grade': 'Оцінка',
            'feedback': 'Коментар викладача'
        }