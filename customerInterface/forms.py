from datetime import date,datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import todo, task

class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['title','end_date',"content","complete"]

        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date','class': 'toDoField', 'min': date.today().strftime('%Y-%m-%d')}),
            'content': forms.Textarea(attrs={"rows": 4, "cols":20, 'class': 'toDoField'}),
            'title': forms.TextInput(attrs={'class': 'toDoField'})}
        
    def __init__(self, *args, **kwargs):
        super(ToDoItemForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].initial = datetime.today().strftime('%Y-%m-%d')
        self.fields['content'].required = False

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        error_messages={
            'required': 'Please enter a username.',
            'max_length': 'Username must be 150 characters or fewer.',
            'invalid': 'Please enter a valid username.',
        }
    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'loginField'}),
        error_messages={
            'password_mismatch': 'The two password fields didn’t match.',
        },
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'loginField'}),
    )
               
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'loginField'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginField passwordField'}), required=True)

    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class taskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ['title', 'description', 'start_time','start_date','end_date', 'end_time','repeat','all_day']

        widgets = {
            'description': forms.Textarea(attrs={"rows": 6, "cols":20, 'class': 'taskField'}),
            'title': forms.TextInput(attrs={'class': 'taskField'}),
            'end_time': forms.TimeInput(attrs={'type':'time','class': 'timeField'}),
            'start_date': forms.DateInput(attrs={'type': 'date','class': 'dateField'}),
            'end_date': forms.DateInput(attrs={'type':'date','class': 'dateField'}),
            'start_time': forms.TimeInput(attrs={'type':'time','class': 'timeField'}),
            'repeat': forms.Select(attrs={'class': 'taskField'}),
            'all_day': forms.CheckboxInput(attrs={'class': 'allDayBox','style': 'width: 20px; height: 20px;'})
        }

    def __init__(self, *args, **kwargs):
        super(taskForm, self).__init__(*args, **kwargs)

        self.fields['start_date'].initial = datetime.today().strftime('%Y-%m-%d')
        self.fields['start_time'].initial = datetime.now().strftime('%H:%M')
        self.fields['end_date'].initial = datetime.today().strftime('%Y-%m-%d')
        self.fields['end_time'].initial = datetime.now().strftime('%H:%M')

        for field_name in ['description', 'all_day', 'repeat','start_time','end_time']:
            self.fields[field_name].required = False

        self.fields['all_day'].widget.attrs.update({
            'onclick': 'toggleTimeFields(this)'
        })




