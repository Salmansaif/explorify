from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class": "form-control input-lg", "placeholder": "Email"}))


class LoginForm(forms.Form):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class": "form-control input-lg", "placeholder": "Email"}))
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control input-lg", "placeholder": "Password"}))


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({"class": "form-control input-lg", "placeholder": "Full Name"})
        self.fields['full_name'].label=""
        self.fields['email'].widget.attrs.update({"class": "form-control input-lg", "placeholder": "Email"})
        self.fields['email'].label=""

    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control input-lg", "placeholder": "Password"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control input-lg", "placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # Send confirmation email
        if commit:
            user.save()
        return user






# class RegisterForm(forms.Form):
# 	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}))
# 	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Name"}))
# 	password = forms.CharField(widget=forms.PasswordInput)
# 	password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

# 	def clean_username(self):
# 		username = self.cleaned_data.get("username")
# 		qs = User.objects.filter(username=username)
# 		if qs.exists():
# 			raise forms.ValidationError("Username is taken")
# 		return username

# 	def clean_email(self):
# 		email = self.cleaned_data.get("email")
# 		qs = User.objects.filter(email=email)
# 		if qs.exists():
# 			raise forms.ValidationError("email is taken")
# 		return email

# 	def clean(self):
# 		data = self.cleaned_data
# 		password = self.cleaned_data.get("password")
# 		password_confirm = self.cleaned_data.get("password_confirm")
# 		if password != password_confirm:
# 			raise forms.ValidationError("Password didn't match!")
# 		return data