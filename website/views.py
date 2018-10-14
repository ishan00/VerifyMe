from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import Users,Resume,Section,Point,Conversation,Message,Notification,Passwords
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def login_view(request):

	if request.session.get('user') != None:
		return redirect('/home')

	if request.method == "POST":

		if request.POST["type"] == "login":

			roll = request.POST["roll"]
			pasw = request.POST["password"]

			if Passwords.objects.filter(roll_number = roll, password = pasw).count() > 0:

				# Valid Login/Password

				user = Users.objects.get(roll_number = roll)

				request.session['user'] = user.roll_number

				return redirect('/home')

			else:

				return render(request, 'website/login.html', {'login_status':'Incorrect roll number or password'})

		elif request.POST["type"] == "registration":

			roll = request.POST['roll']
			name = request.POST['name']
			pasw = request.POST['password']
			dept = request.POST['department']

			if Users.objects.filter(roll_number = roll).count() == 0:

				Passwords.objects.create(roll_number = roll, password = pasw)
				user = Users.objects.create(roll_number = roll, name = name, department = dept)

				request.session['user'] = user.roll_number

				return redirect('/home')

			else:

				return render(request, 'website/login.html', {'registration_status':'This roll number already exists'})

	else:

		return render(request, 'website/login.html', {})		


def logout_view(request):

	if request.session.get('user') != None:
		del request.session['user']

	return redirect('/')

def home_view(request):

	if request.session.get('user') != None:

		logged_user_roll = request.session['user']
		
		user = Users.objects.get(roll_number = logged_user_roll)
		resume_list = Resume.objects.filter(user = user).order_by("timestamp")

		return render(request, 'website/home_page.html', {'user':user, 'resume_list': resume_list})

	else:

		return redirect('/')

@csrf_exempt
def create_new_resume(request):
	
	return render(request, 'website/home_page.html', {})


@csrf_exempt
def view_resume(request):

	print("REQUEST")
	id = request.POST["id"]
	resume = Resume.objects.get(id = id)
	list_of_sections = Section.objects.filter(resume_id = id)
	list_of_points = Point.objects.filter(resume_id = id)

	return render(request, 'website/display_resume.html', {'resume':resume, 'section':list_of_sections, 'point':list_of_points})

@csrf_exempt
def add_resume_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)

			title = request.POST['title']

			new_resume = Resume.objects.create(user = user, title = title)
			
			resume_list = Resume.objects.filter(user = user).order_by("timestamp")

			resume_list = [ model_to_dict(obj) for obj in resume_list]

			return JsonResponse({'resume':resume_list})

	else:

		return redirect('/')

def view_messages(request):
	user = 1
	conv_id = Conversation.objects.filter(Q(user1 = user) | Q(user2 = user))
	messages = Message.objects.filter(conversation_id__in=conv_id)
	return render(request, 'website/display_messages.html', {'user':user, 'messages':messages, 'conversations':conv_id})

def view_notifications(request):
	notifications = Notification.objects.all()
	return render(request, 'website/display_notifications.html', {'notifications':notifications})
