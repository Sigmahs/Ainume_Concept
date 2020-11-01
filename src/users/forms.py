from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField
from users.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text="Required. Enter a valid email address")
	first_name = forms.CharField(max_length=30, help_text="Required. Please enter first name")
	last_name = forms.CharField(max_length=30, help_text="Required. Please enter last name")
	phone_number = PhoneNumberField()



	class Meta:
		model = Account
		fields = ("email", "username", "first_name", "last_name", "phone_number", "password1", "password2")


class AccountAuthenticationForm(forms.Form):

	email = forms.CharField(label='Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	fields = ['email', 'password']

	def clean(self):
			if self.is_valid():
				email = self.cleaned_data['email']
				password = self.cleaned_data['password']

				user = authenticate(email=email, password=password)
				if not user:
					raise forms.ValidationError("Incorrect login, please try again")

class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.' % account.username)