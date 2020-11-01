from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import MyAccountManager

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			context['success_message'] = "Successfully registered an account! Please sign in."
			return redirect('home')
		else:
			context['registration_form'] = form
			return render(request, 'users/register.html', context)
	else:
		form = RegistrationForm()
		context['registration_form'] = form
		return render(request, 'users/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("home")
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				return redirect("home")
		else:
			messages.error(request, 'Invalid Username/Password')
	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form
	return render(request, 'users/login.html', context)

def account_view(request):

	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Successfully Updated!"
			return render(request, 'users/account.html', context)

	else:
		form = AccountUpdateForm(
		initial = {
			"email": request.user.email,
			"username": request.user.username
				}
			)
		context['account_form'] = form
		return render(request, 'users/account.html', context)

			

