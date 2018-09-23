from django.urls import path
from . import views

urlpatterns = [
	path('', views.home_page, name = 'home_page'),
	path('resume/new', views.create_new_resume, name = 'create_new_resume'),
	path('resume/<int:id>/', views.view_resume, name = 'view_resume'),
	path('messages/', views.view_messages, name = 'view_messages'),
	path('notifications/', views.view_notifications, name = 'view_notifications'),
]