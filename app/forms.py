from django import forms
from django.contrib.auth.models import User

from app.models import Order, Comment, Profile

allowed_choices = [(i, str(i)) for i in range(1, 11)]


class UpdateCountForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=allowed_choices, coerce=int)


class UserProfileForm(forms.Form):
    pass


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'delivery_address', 'issue_point', 'total_cost']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_point': forms.Select(attrs={'class': 'form-control'}),
        }


class AddCommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mark'].empty_label = 'Unselected'

    class Meta:
        model = Comment
        fields = ['id', 'text', 'mark']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control','placeholder':'Your text'}),
            'mark': forms.Select(attrs={'class': 'form-control'}),
        }


class AddProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'profile_pic','location']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
