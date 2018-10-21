from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import Users,Resume,Section,Point,Conversation,Message,Notification,Passwords,Request
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

		resume_list = Resume.objects.filter(user = user).order_by("-timestamp")

		if request.session.get('resume_id') != None:
			del request.session['resume_id']

		request_list = Request.objects.filter(user_receiver = user)

		notifications = Notification.objects.filter(user_receiver = user)

		return render(request, 'website/home_page.html', {'user':user, 'resume_list': resume_list, 'request_list': request_list, 'notifications':notifications})

	else:

		return redirect('/')


@csrf_exempt
def view_resume(request):

	if request.session.get('user') != None:

		logged_user_roll = request.session['user']
		user = Users.objects.get(roll_number = logged_user_roll)


		if request.session.get('resume_id') != None:

			resume = Resume.objects.get(id = request.session['resume_id'])
			
			sections = Section.objects.filter(resume = resume)
			section_list = [model_to_dict(obj) for obj in sections]
			for i in range(len(sections)):
				points = Point.objects.filter(section = sections[i])
				section_list[i]['points'] = [ model_to_dict(obj) for obj in points]

			notifications = Notification.objects.filter(user_receiver = user)

			return render(request, 'website/resume.html', {'user':user, 'resume': resume, 'sections' : section_list, 'notifications':notifications})


		elif request.method == "POST":
			
			resume_id = request.POST['id']

			if Resume.objects.filter(id = resume_id, user = user).count != 0:

				resume = Resume.objects.get(id = resume_id)
				request.session['resume_id'] = resume_id

				sections = Section.objects.filter(resume = resume)
				section_list = [model_to_dict(obj) for obj in sections]
				for i in range(len(sections)):
					points = Point.objects.filter(section = sections[i])
					section_list[i]['points'] = [ model_to_dict(obj) for obj in points]

				notifications = Notification.objects.filter(user_receiver = user)

				return render(request, 'website/resume.html', {'user':user, 'resume': resume, 'sections' : section_list, 'notifications':notifications})

		else:

			return redirect('/home')

	else:

		return redirect('/')


@csrf_exempt
def add_resume_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)

			title = request.POST['title']

			new_resume = Resume.objects.create(user = user, title = title)
			
			#resume_list = Resume.objects.filter(user = user).order_by("timestamp")

			#resume_list = [ model_to_dict(obj) for obj in resume_list]

			#return JsonResponse({'resume':resume_list})

			return redirect('/home')

	else:

		return redirect('/')


@csrf_exempt
def delete_resume_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)

			resume_id = request.POST['resume_id']

			Resume.objects.filter(user = user, id=resume_id).delete()


			return redirect('/home')

	else:

		return redirect('/')



@csrf_exempt
def add_point_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			print (request)

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)

			content = request.POST['content']
			section_id = request.POST['section_id']

			print (content,section_id)

			section = Section.objects.get(id=section_id)
			new_Point = Point.objects.create(section = section, content = content)
			
			return redirect('/resume')

	else:

		return redirect('/')

@csrf_exempt
def add_section_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			if request.session.get('resume_id') != None:
				resume = Resume.objects.get(id = request.session['resume_id'])

			title = request.POST['title']
			# type = re

			new_section = Section.objects.create(resume = resume, title = title)

			sections = Section.objects.filter(resume = resume)
			section_list = [model_to_dict(obj) for obj in sections]
			for i in range(len(sections)):
				points = Point.objects.filter(section = sections[i])
				section_list[i]['points'] = [ model_to_dict(obj) for obj in points]

			return redirect('/resume')
	else:

		return redirect('/')

@csrf_exempt
def delete_section_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			print(request.POST)
			section_id = request.POST['section_id']

			Section.objects.filter(id=section_id).delete()


			return redirect('/resume')

	else:

		return redirect('/')



@csrf_exempt
def view_messages(request):

	if request.session.get('user') != None:

		logged_user_roll = request.session['user']
		user = Users.objects.get(roll_number = logged_user_roll)

		notifications = Notification.objects.filter(user_receiver = user)

		conversations = Conversation.objects.filter(Q(user1 = user) | Q(user2 = user))

		if len(conversations) > 0:
			
			latest_conversation = conversations[0].id

			messages = Message.objects.filter(conversation_id = latest_conversation)

		else:
			messages = ''

		return render(request, 'website/messages.html', {'user':user, 'notifications':notifications, 'conversations':conversations, 'messages':messages})

		'''
		if request.session.get('resume_id') != None:
			resume = Resume.objects.get(id = request.session['resume_id'])

		title = request.POST['title']
		# type = re

		new_section = Section.objects.create(resume = resume, title = title)

		sections = Section.objects.filter(resume = resume)
		section_list = [model_to_dict(obj) for obj in sections]
		for i in range(len(sections)):
			points = Point.objects.filter(section = sections[i])
			section_list[i]['points'] = [ model_to_dict(obj) for obj in points]

		return redirect('/resume')
		'''
	else:

		return redirect('/')
