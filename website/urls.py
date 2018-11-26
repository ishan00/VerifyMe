from django.urls import path
from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	re_path(r'^media/(?P<path>.*)$', views.protected_serve, {'document_root': settings.MEDIA_ROOT}),
	path('', views.login_view, name = 'login_view'),
	path('home/',views.home_view, name = 'home_view'),
	path('profile/',views.profile_view, name = 'profile_view'),
	path('resume/', views.view_resume, name = 'view_resume'),
	path('messages/', views.view_messages, name = 'view_messages'),
	path('logout/', views.logout_view, name = 'logout_view'),
	path('add_resume/', views.add_resume_view, name = 'add_resume_view'),
	path('delete_resume/', views.delete_resume_view, name = 'delete_resume_view'),
	path('add_section/', views.add_section_view, name = 'add_section_view'),
	path('delete_section/', views.delete_section_view, name = 'delete_section_view'),
	path('add_point/', views.add_point_view, name = 'add_point_view'),
	path('delete_point/', views.delete_point_view, name = 'delete_point_view'),
	path('add_message/', views.home_view, name = 'logout_view'),
	path('add_request/', views.add_request_view, name = 'add_request_view'),
	path('request_action/', views.request_action_view, name = 'request_action_view'),
	path('upload/', views.upload, name = 'upload'),
	path('get_files/', views.get_files, name = 'get_files'),
	path('delete_file/', views.delete_file, name = 'delete_file'),
	path('mark_as_read/', views.mark_as_read, name = 'mark_as_read'),
	path('redirect_request/', views.redirect_request_view, name = 'redirect_request_view'),
	path('reorder_section/', views.reorder_section_view, name = 'reorder_section_view'),
	path('send_message/', views.send_message, name = 'send_message'),
	path('change_conversation/', views.change_conversation, name = 'change_conversation'),
	path('change_list/', views.change_list, name = 'change_list'),
	path('create_conversation/', views.create_conversation, name = 'create_conversation'),
	path('reset_password/', views.reset_password, name = 'reset_password'),
	path('update_profile/', views.update_profile, name = 'update_profile'),
	path('upload_profile_image/', views.upload_profile_image, name = 'upload_profile_image'),
	path('open_conversation/', views.open_conversation, name = 'open_conversation'),
	path('transfer_privilege/', views.transfer_privilege, name = 'transfer_privilege')
]
