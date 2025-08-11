from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 


class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'date_joined', 'last_login'] 
        labels = {
            'email': 'Email',
            'date_joined': 'Date Joined',
            'last_login': 'Last Login',
        }

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)

        # Disable specific fields
        disabled_fields = ['username', 'email', 'date_joined', 'last_login']
        for field in disabled_fields:
            self.fields[field].disabled = True
            self.fields[field].widget.attrs.update({
                'class': 'w-full border-gray-300 rounded-md shadow-sm p-2 bg-gray-100',
            })

        # Style editable fields
        for field in ['first_name', 'last_name']:
            self.fields[field].widget.attrs.update({
                'class': 'mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            })






