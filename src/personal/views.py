from django.shortcuts import render
from users.models import Account
# Create your views here.

def home_screen_view(request):

	context = {}
	#context['some_string'] = "this is a string that I'm passing through the view"
	#context['some_number'] = 12345

	#list_of_values = []
	#list_of_values.append("1st")
	#list_of_values.append("2st")
	#list_of_values.append("3st")
	#context['list_of_values'] = list_of_values

	# questions = Question.objects.all()
	# context['questions'] = questions

	accounts = Account.objects.all()
	context['accounts'] = accounts


	return render(request, "personal/home.html", context)
