from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, first_name, last_name, phone_number, password=None):
		if not email:
			raise ValueError("Field cannot be left empty")
		if not username:
			raise ValueError("Field cannot be left empty")
		if not first_name:
			raise ValueError("Field cannot be left empty")
		if not last_name:
			raise ValueError("Field cannot be left empty")
		if not phone_number:
			raise ValueError("Field cannot be left empty")

		user = self.model(
			   email=self.normalize_email(email),
			   username=username,
			   phone_number=phone_number,
			   first_name=first_name,
			   last_name=last_name
			   )


		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			first_name='admin',
			last_name='admin',
			phone_number='8053777078',
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	email					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_superuser			= models.BooleanField(default=False)
	is_staff				= models.BooleanField(default=False)
	first_name 				= models.CharField(max_length=30)
	last_name 				= models.CharField(max_length=30)
	phone_number			= PhoneNumberField()


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username',]

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

