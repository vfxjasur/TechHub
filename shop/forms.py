from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import ContactMessage, Order, UserProfile

User = get_user_model()


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+998', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 5, 'required': True}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'email', 'address', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+998', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 3, 'placeholder': 'Необязательно'}),
            'comment': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 3}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input'})
            if field.startswith('new_password'):
                self.fields[field].min_length = 8


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте имя пользователя'}))
    full_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше имя'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create or update profile with full_name
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.full_name = self.cleaned_data['full_name']
            profile.save()
        return user
