from django import forms

from app.models import Order

allowed_choices = [(i, str(i)) for i in range(1, 11)]


class UpdateCountForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=allowed_choices, coerce=int)


class UserProfileForm(forms.Form):
    pass


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'delivery_address', 'issue_point','total_cost']

