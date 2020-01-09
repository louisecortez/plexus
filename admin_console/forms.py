from django import forms
from django.contrib.auth import authenticate

from admin_console.models import SurveyFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = SurveyFile
        fields = ['city', 'file', 'description', 'date_collected']

class MappingForm(forms.Form):
    submission_id = forms.ChoiceField(choices=(), required=True)
    submission_time = forms.ChoiceField(choices=(), required=True)
    survey_file = forms.ChoiceField(choices=(), required=True)
    barangay = forms.ChoiceField(choices=(), required=True)
    address = forms.ChoiceField(choices=(), required=True)
    address_extra = forms.ChoiceField(choices=(), required=True)
    income = forms.ChoiceField(choices=(), required=True)
    education = forms.ChoiceField(choices=(), required=True)
    num_cars = forms.ChoiceField(choices=(), required=True)
    years_residing = forms.ChoiceField(choices=(), required=True)
    own_or_rent = forms.ChoiceField(choices=(), required=True)
    num_members = forms.ChoiceField(choices=(), required=True)
    role = forms.ChoiceField(choices=(), required=True)
    age = forms.ChoiceField(choices=(), required=True)
    occupation = forms.ChoiceField(choices=(), required=True)
    job = forms.ChoiceField(choices=(), required=True)
    income_range = forms.ChoiceField(choices=(), required=True)
    trip_purpose = forms.ChoiceField(choices=(), required=True)
    dest_barangay = forms.ChoiceField(choices=(), required=True)
    dest_address = forms.ChoiceField(choices=(), required=True)
    dest_address_extra = forms.ChoiceField(choices=(), required=True)
    trip_mode = forms.ChoiceField(choices=(), required=True)
    travel_time = forms.ChoiceField(choices=(), required=True)
    gas_or_diesel = forms.ChoiceField(choices=(), required=True)
    fuel_cost = forms.ChoiceField(choices=(), required=True)
    fare = forms.ChoiceField(choices=(), required=True)
    is_flood_prone = forms.ChoiceField(choices=(), required=True)
    will_cancel = forms.ChoiceField(choices=(), required=True)
    new_time = forms.ChoiceField(choices=(), required=True)
    new_cost = forms.ChoiceField(choices=(), required=True)

    def __init__(self, choices, *args, **kwargs):
        super(MappingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            field.choices = choices

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)