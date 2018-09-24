from django.urls import path
from . import views

urlpatterns = [
	path('', views.login_view, name = 'login_view'),
	path('home/',views.home_view, name = 'home_view'),
	path('resume/new', views.create_new_resume, name = 'create_new_resume'),
	path('resume/<int:id>/', views.view_resume, name = 'view_resume'),
	path('messages/', views.view_messages, name = 'view_messages'),
	path('notifications/', views.view_notifications, name = 'view_notifications'),
	path('logout/', views.logout_view, name = 'logout_view'),
]