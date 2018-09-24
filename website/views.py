from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Users,Resume,Section,Point,Conversation,Message,Notification


def login_view(request):

	if request.method == "POST":

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			return redirect('home_view')
		else:
			return render(request, 'website/login.html', {'meta':'Incorrect Username / Password'})

	else:

		return render(request, 'website/login.html', {})

def logout_view(request):
	logout(request)
	return redirect('login_view')

@login_required()
def home_view(request):
	user_list = Users.objects.all()
	return render(request, 'website/home_page.html', {'user_list':user_list})


@login_required()
def create_new_resume(request):
	
	return render(request, 'website/home_page.html', {})


@login_required()
def view_resume(request,id):

	resume = Resume.objects.get(id = id)
	list_of_sections = Section.objects.filter(resume_id = id)
	list_of_points = Point.objects.filter(resume_id = id)

	return render(request, 'website/display_resume.html', {'resume':resume, 'section':list_of_sections, 'point':list_of_points})


@login_required()
def view_messages(request):
	user = 1
	conv_id = Conversation.objects.filter(Q(user1 = user) | Q(user2 = user))
	messages = Message.objects.filter(conversation_id__in=conv_id)
	return render(request, 'website/display_messages.html', {'user':user, 'messages':messages, 'conversations':conv_id})


@login_required()
def view_notifications(request):
	notifications = Notification.objects.all()
	return render(request, 'website/display_notifications.html', {'notifications':notifications})