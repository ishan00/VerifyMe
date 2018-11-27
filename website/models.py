from django.db import models
from django.utils import timezone

POINT_TYPE = (
	('BU','Bullet'),
	('BL','Block'),
	('M2','2 Columns'),
	('M3','3 Columns'),
	('M4','4 Columns'),
)

POINT_STATUS = (
	('N','None'),
	('F','Freeze'),
	('P','Pending'),
	('V','Verified'),
	('R','Rejected'),
)

LIST_OF_DEPARTMENTS = (
	('CS','Computer Science and Engineering'),
	('MA','Mathematics'),
	('EE','Electrical Engineering'),
	('CE','Civil Engineering'),
)

LIST_OF_YEARS = (
	('B1','B.Tech. 1st Year'),
	('B2','B.Tech. 2nd Year'),
	('B3','B.Tech. 3rd Year'),
	('B4','B.Tech. 4th Year'),
	('M1','M.Tech. 1st Year'),
	('M2','M.Tech. 2nd Year'),
)

class Passwords(models.Model):

	roll_number = models.CharField(max_length = 30)

	password = models.CharField(max_length = 30)

	def __str__(self):
		return str(self.id)


class Users(models.Model):

	roll_number = models.CharField(max_length = 30)
	name = models.CharField(max_length = 50)
	department = models.CharField(max_length = 2, choices = LIST_OF_DEPARTMENTS)
	#year = models.CharField(max_length = 2,choices = LIST_OF_YEARS)
	image = models.CharField(max_length = 100, default = 'profiles/default/default.png')
	privilege = models.BooleanField(default = False)
	position = models.CharField(max_length = 100, null = True)

	def __str__(self):
		return str(self.id)

class Resume(models.Model):

	user = models.ForeignKey('Users', on_delete = models.CASCADE)
	title = models.CharField(max_length = 100, default = '')

	timestamp = models.DateTimeField(auto_now_add = True, null = True)
	status = models.IntegerField(default = 2) #1 for rejected, 2 for pending, 3 for verified

	def __str__(self):
		return str(self.id)

class Section(models.Model):

	resume = models.ForeignKey('Resume', on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)
	type = models.CharField(max_length = 2, choices = POINT_TYPE, default = 'BU')

	def __str__(self):
		return str(self.id)

class Point(models.Model):

	#resume_id = models.ForeignKey('Resume', on_delete = models.CASCADE)
	section = models.ForeignKey('Section', on_delete = models.CASCADE)

	position = models.IntegerField(editable = False, default = 0)

	type = models.CharField(max_length = 2, choices = POINT_TYPE, editable = False, default = 'BU')

	status = models.CharField(max_length = 1, choices = POINT_STATUS, default = 'P')
	
	content = models.TextField(default = '')

	comment = models.TextField(default = '')

	timestamp = models.DateTimeField(auto_now_add = True, null = True)

	def __str__(self):
		return str(self.id)

class Request(models.Model):
	
	sender = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_request_sender')
	receiver = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_request_receiver')

	point = models.ForeignKey('Point', on_delete = models.CASCADE)
	status = models.BooleanField(editable = True, default = True)

	timestamp = models.DateTimeField(auto_now_add = True, null = True)

	def __str__(self):
		return str(self.id)

class Conversation(models.Model):

	user1 = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_conversation_user1')
	user2 = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_conversation_user2')

	timestamp = models.DateTimeField(auto_now_add = True, null = True)

	def __str__(self):
		return str(self.id)


class Message(models.Model):

	conversation = models.ForeignKey('Conversation', on_delete = models.CASCADE)
	sender = models.ForeignKey('Users', on_delete = models.CASCADE)

	content = models.TextField(default = '')

	timestamp = models.DateTimeField(auto_now_add = True, null = True)

	def __str__(self):
		return str(self.id)

class Notification(models.Model):

	sender = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_notification_sender')
	receiver = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_notification_receiver')

	n_type = models.IntegerField(editable = True, null = False)

	point = models.ForeignKey('Point', on_delete = models.CASCADE)

	seen = models.BooleanField(editable = True, default = False)

	timestamp = models.DateTimeField(auto_now_add = True, null = True, editable = True)

	def __str__(self):
		return str(self.id)












