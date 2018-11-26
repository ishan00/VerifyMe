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
from datetime import datetime, timezone

def protected_serve(request,path,document_root=None,show_indexes=False):
	
	if request.session.get('user') != None:
		logged_user_roll = request.session['user']
		user = Users.objects.get(roll_number = logged_user_roll)
		point_id = path.split('/')[0].strip()
		point = Point.objects.get(id=point_id)
		if point.section.resume.user != user:
			requests = Request.objects.filter(receiver=user)
			found = False
			for request1 in requests:
				if request1.point == point:
					found = True
			if not found:
				return view_resume(request, "Access denied")
		return serve(request,path,document_root,show_indexes)

	else:
		return redirect('/')


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

		notifications = Notification.objects.filter(receiver = user).order_by("-timestamp")

		count = 0
		for n in notifications:
			if not n.seen:
				count += 1

		requests = Request.objects.filter(receiver = user).order_by("-timestamp")
		
		request_list = []
		for request1 in requests :
			request_list.append({'id' : request1.id,'sender' : request1.sender.name, 'point_content' : request1.point.content, 'point_id' : request1.point.id})

		privileged_user = Users.objects.filter(privilege = True)

		# print(request_list)

		return render(request, 'website/home_page.html', {'user':user, 'resume_list': resume_list, 'request_list': request_list, 'notifications':notifications, 'notification_count':count, 'privileged_user':privileged_user})

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

			notifications = Notification.objects.filter(receiver = user).order_by("-timestamp")

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

				notifications = Notification.objects.filter(receiver = user).order_by("-timestamp")

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

# def sort_function(x):
# 	if(isinstance(x['message'], dict)):
# 		return x['c'].timestamp
# 	else:
# 		return x['c'].timestamp


@csrf_exempt
def view_messages(request):

	if request.session.get('user') != None:

		logged_user_roll = request.session['user']
		user = Users.objects.get(roll_number = logged_user_roll)

		notifications = Notification.objects.filter(receiver = user)

		conversations = Conversation.objects.filter(Q(user1 = user) | Q(user2 = user)).order_by('-timestamp')

		conversations_list = []

		for conversation in conversations:
			messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
			if(len(messages)==0):
				conversations_list.append({'c': conversation, 'message':{'content' : ''}})
			else:
				conversations_list.append({'c': conversation, 'message':messages[0]})

		conversations_list.sort(key=lambda x: x['c'].timestamp, reverse=True)

		if len(conversations) > 0:
			
			if (request.session.get('conversation_id') != None):
				latest_conversation = request.session['conversation_id']
			else:
				latest_conversation = conversations[0].id
				request.session['conversation_id'] = latest_conversation

			latest_conversation = Conversation.objects.get(id=latest_conversation)


			messages = Message.objects.filter(conversation = latest_conversation)

		else:
			messages = ''

		return render(request, 'website/messages.html', {'user':user, 'notifications':notifications, 'conversations':conversations_list, 'messages':messages})

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
def send_message(request):

	if request.session.get('user') != None:

		logged_user_roll = request.session['user']
		sender = Users.objects.get(roll_number = logged_user_roll)

		conversation_id = request.session['conversation_id']
		conversation = Conversation.objects.get(id=conversation_id)

		content = request.POST['message']
		Message.objects.create(conversation=conversation, sender=sender, content=content)

		conversation.timestamp = datetime.now()
		conversation.save()

		return redirect('/messages')

	else:

		return redirect('/')

@csrf_exempt
def change_conversation(request):

	if request.session.get('user') != None:

		conversation_id = request.POST['conversation_id']
		conversation = Conversation.objects.get(id=conversation_id)

		request.session['conversation_id']=conversation_id


		return redirect('/messages')

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
			Notification.objects.create(sender=sender, receiver=receiver, n_type=2, point=point, seen=False)
			
			return redirect('/resume')

	else:

		return redirect('/')

@csrf_exempt
def redirect_request_view(request):
	
	if request.session.get('user') != None:

		if request.method == "POST":


			logged_user_roll = request.session['user']

			roll_number = request.POST['roll_number']
			new_receiver = Users.objects.get(roll_number = roll_number)
			
			request_id = request.POST['redirectModalID']

			request1 = Request.objects.get(id=request_id)
			request1.receiver = new_receiver
			request1.save()

			Notification.objects.create(sender=request1.sender, receiver=new_receiver, n_type=2, point=request1.point, seen=False)
			
			return redirect('/home')

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
				Notification.objects.create(sender=sender, receiver=point.section.resume.user, n_type=0, point=point, seen=False)
			elif(verified == '0'):
				comment = request.POST['comment']
				point.status = 'R'
				point.comment = comment
				Notification.objects.create(sender=sender, receiver=point.section.resume.user, n_type=1, point=point, seen=False)

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

def delete_file(request):	
	if request.session.get('user') != None:

		if request.method == "GET":
			point_id = request.GET['id']
			file_name = request.GET['path']

			print("fwsf")

			path = Path("media/"+point_id+'/'+file_name)

			if(path.exists()):
				os.remove("media/"+point_id+'/'+file_name)
		
			return JsonResponse({})


	else:
		return redirect('/')


def mark_as_read(request):	
	if request.session.get('user') != None:

		if request.method == "GET":

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)			
			notifications = Notification.objects.filter(receiver = user)
			for notification in notifications:
				notification.seen = True
				notification.save()		
			return JsonResponse({})


	else:
		return redirect('/')

def change_list(request):	
	if request.session.get('user') != None:

		if request.method == "GET":

			logged_user_roll = request.session['user']
			user = Users.objects.get(roll_number = logged_user_roll)

			text = request.GET['text']
			length = len(text)
			users = Users.objects.all()
			users = [model_to_dict(obj) for obj in users]
			user_list = []

			for user in users:
				if user['roll_number'][:length] == text or user['name'][:length] == text:
					print(user)
					user_list.append({'key': user['name'] + ' ' + user['roll_number'], 'value':user['roll_number']})
	
			return JsonResponse({'user_list' : user_list})


	else:
		return redirect('/')

@csrf_exempt
def create_conversation(request):	
	if request.session.get('user') != None:

		if request.method == "POST":

			logged_user_roll = request.session['user']
			user1 = Users.objects.get(roll_number = logged_user_roll)

			roll_number = request.POST['roll_number']
			user2 = Users.objects.get(roll_number=roll_number)
			conversation1 = Conversation.objects.filter(user1=user1, user2=user2)
			conversation2 = Conversation.objects.filter(user1=user2, user2=user1)
			if(not conversation1 and not conversation2):
				Conversation.objects.create(user1=user1, user2=user2)
			
			return redirect('/messages/')


	else:
		return redirect('/')