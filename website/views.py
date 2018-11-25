from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .models import Users,Resume,Section,Point,Conversation,Message,Notification,Passwords,Request
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.core.files.storage import default_storage
import os
from pathlib import Path

def protected_serve(request,path,document_root=None,show_indexes=False):
	print("Maja aa gaya")
	return serve(request,path,document_root,show_indexes)


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

		# request_list = Request.objects.filter(receiver = user)

		notifications = Notification.objects.filter(receiver = user)

		requests = Request.objects.filter(receiver = user).order_by("-timestamp")
		
		request_list = []
		for request1 in requests :
			request_list.append({'id' : request1.id,'sender' : request1.sender.name, 'point_content' : request1.point.content, 'point_id' : request1.point.id})

		# print(request_list)

		return render(request, 'website/home_page.html', {'user':user, 'resume_list': resume_list, 'request_list': request_list, 'notifications':notifications})

	else:

		return redirect('/')


@csrf_exempt
def view_resume(request, alert = ""):

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

			notifications = Notification.objects.filter(receiver = user)

			privileged_user = Users.objects.filter(privilege = True)


			
			return render(request, 'website/resume.html', {'user':user, 'resume': resume, 'sections' : section_list, 'notifications':notifications, 'privileged_user' : privileged_user, 'alert' : alert})


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

				notifications = Notification.objects.filter(receiver = user)

				privileged_user = Users.objects.filter(privilege = True)

				return render(request, 'website/resume.html', {'user':user, 'resume': resume, 'sections' : section_list, 'notifications':notifications, 'privileged_user' : privileged_user, 'alert' : alert})

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

			# print (request)

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)

			content = request.POST['content']
			section_id = request.POST['section_id']

			# print (content,section_id)

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

			# print(request.POST)
			section_id = request.POST['section_id']

			Section.objects.filter(id=section_id).delete()


			return redirect('/resume')

	else:

		return redirect('/')

@csrf_exempt
def delete_point_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":

			# print(request.POST)
			point_id = request.POST['point_id']

			Point.objects.filter(id=point_id).delete()


			return redirect('/resume')

	else:

		return redirect('/')




@csrf_exempt
def view_messages(request):

	if request.session.get('user') != None:

		logged_user_roll = request.session['user']
		user = Users.objects.get(roll_number = logged_user_roll)

		notifications = Notification.objects.filter(receiver = user)

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

@csrf_exempt
def add_request_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":


			logged_user_roll = request.session['user']
			sender = Users.objects.get(roll_number = logged_user_roll)

			roll_number = request.POST['roll_number']
			receiver = Users.objects.get(roll_number = roll_number)
			
			point_id = request.POST['sendModalID']
			point = Point.objects.get(id = point_id)

			Request.objects.create(sender = sender, receiver = receiver,  point = point)
			
			return redirect('/resume')

	else:

		return redirect('/')


@csrf_exempt
def request_action_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":


			logged_user_roll = request.session['user']
			sender = Users.objects.get(roll_number = logged_user_roll)

			request_id = request.POST['request_id']
			verified = request.POST['verified']

			request1 = Request.objects.get(id=request_id)
			point = request1.point
			if(verified == '1'):
				point.status = 'V'
			elif(verified == '0'):
				comment = request.POST['comment']
				point.status = 'R'
				point.comment = comment

			point.save()
			request1.delete()


			return redirect('/')



@csrf_exempt
def upload(request):	
	if request.session.get('user') != None:

		if request.method == "POST":
			files = request.FILES.getlist('file')
			point_id = request.POST['pointID']
			point = Point.objects.get(id=point_id)
			logged_user_roll = request.session['user']

			if point.section.resume.user.roll_number != logged_user_roll:
				return view_resume(request, "Unable to upload")

			for file in files:
				file_name = default_storage.save(point_id + '/' + file.name, file)
			return view_resume(request, "Successfully uploaded")

	else:
		return redirect('/')

def get_files(request):	
	if request.session.get('user') != None:

		if request.method == "GET":
			if(request.GET['point'] == '0'):
				request_id = request.GET['id']
				request = Request.objects.get(id=request_id)
				point_id = str(request.point.id)
			else:
				point_id = request.GET['id']

			path = Path("media/"+point_id)

			file_list = [];
			if(path.is_dir()):
				file_list = os.listdir("media/"+point_id)
		
			return JsonResponse({'data': file_list, 'point_id' : point_id})


	else:
		return redirect('/')