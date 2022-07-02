from django import forms

from app.models import Order, Comment

allowed_choices = [(i, str(i)) for i in range(1, 11)]


class UpdateCountForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=allowed_choices, coerce=int)


class UserProfileForm(forms.Form):
    pass


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'delivery_address', 'issue_point', 'total_cost']


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
