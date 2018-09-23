from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Users,Resume,Section,Point

def home_page(request):
	user_list = User.objects.all()
	return render(request, 'website/home_page.html', {'user_list':user_list})

