from django import forms

allowed_choices = [(i, str(i)) for i in range(1, 11)]


class UpdateCountForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=allowed_choices, coerce=int)

class UserProfileForm(forms.Form):
    pass