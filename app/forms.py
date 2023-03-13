from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from app.models import Appointment, CustomUser, Customer, Device, Pet, Purpose


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('device_id', 'owner', 'pet')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.none()

        if 'owner' in self.data:
            try:
                owner_id = str(self.data.get('owner'))
                self.fields['pet'].queryset = Pet.objects.filter(
                    owner__id=owner_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['pet'].queryset = self.instance.country.city_set.order_by('name')



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'firstname', 'middlename', 'lastname')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'firstname', 'middlename', 'lastname', 'picture', 'is_active', 'is_superuser')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class AppointmentForm(forms.ModelForm):
    purpose = forms.ChoiceField(choices=Purpose.choices)
    
    class Meta:
        model = Appointment
        fields = ('pet', 'date', 'purpose')
    
    def __init__(self, owner=None, **kwargs):
        super(AppointmentForm, self).__init__(**kwargs)
        if owner:
            self.fields['pet'].queryset = Pet.objects.filter(owner__email=owner.email)