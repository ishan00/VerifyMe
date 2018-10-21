from django.urls import path
from . import views

urlpatterns = [
	path('', views.login_view, name = 'login_view'),
	path('home/',views.home_view, name = 'home_view'),
	path('resume/', views.view_resume, name = 'view_resume'),
	path('messages/', views.view_messages, name = 'view_messages'),
	path('notifications/', views.view_notifications, name = 'view_notifications'),
	path('logout/', views.logout_view, name = 'logout_view'),
	path('add_resume/', views.add_resume_view, name = 'add_resume_view'),
	path('delete_resume/', views.delete_resume_view, name = 'delete_resume_view'),
	path('add_section/', views.add_section_view, name = 'add_section_view'),
	path('delete_section/', views.delete_section_view, name = 'delete_section_view'),
	path('add_point/', views.add_point_view, name = 'add_point_view'),
	path('add_message/', views.home_view, name = 'logout_view'),
]