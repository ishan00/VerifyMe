from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Users,Resume,Section,Point,Conversation,Message,Notification

def home_page(request):
	
	user_list = Users.objects.all()
	print (len(user_list))
	return render(request, 'website/home_page.html', {'user_list':user_list})

def create_new_resume(request):
	
	return render(request, 'website/home_page.html', {})

def view_resume(request,id):
	
	print (request)

	resume = Resume.objects.get(id = id)
	list_of_sections = Section.objects.filter(resume_id = id)
	list_of_points = Point.objects.filter(resume_id = id)

	return render(request, 'website/display_resume.html', {'resume':resume, 'section':list_of_sections, 'point':list_of_points})

def view_messages(request):
	user = 1
	conv_id = Conversation.objects.filter(Q(user1 = user) | Q(user2 = user))
	messages = Message.objects.filter(conversation_id__in=conv_id)
	return render(request, 'website/display_messages.html', {'user':user, 'messages':messages, 'conversations':conv_id})

def view_notifications(request):
	notifications = Notification.objects.all()
	return render(request, 'website/display_notifications.html', {'notifications':notifications})