from django.db import models
from django.utils import timezone

POINT_TYPE = (
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

	privilege = models.BooleanField(editable = False, default = False)
	position = models.CharField(max_length = 100, editable = False, default = '')

	def __str__(self):
		return str(self.id)

class Resume(models.Model):

	user = models.ForeignKey('Users', on_delete = models.CASCADE)
	title = models.CharField(max_length = 100, default = '')

	timestamp = models.DateField(null = True)
	status = models.IntegerField(default = 2) #1 for rejected, 2 for pending, 3 for verified

	def __str__(self):
		return str(self.id)

class Section(models.Model):

	resume_id = models.ForeignKey('Resume', on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)

	def __str__(self):
		return str(self.id)

class Point(models.Model):

	resume_id = models.ForeignKey('Resume', on_delete = models.CASCADE)
	section_id = models.ForeignKey('Section', on_delete = models.CASCADE)

	position_in_list = models.IntegerField(editable = False, default = 0)

	point_type = models.CharField(max_length = 1, choices = POINT_TYPE, editable = False, default = 'N')
	
	content = models.TextField(default = '')

	timestamp = models.DateField(null = True)

class Request(models.Model):
	
	section_id = models.ForeignKey('Section', on_delete = models.CASCADE)
	user_sender = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_request_sender')
	user_receiver = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_request_receiver')

	request_status = models.CharField(max_length = 1, choices = POINT_TYPE, editable = False, default = 'P')

	point = models.ForeignKey('Point', on_delete = models.CASCADE)

	point_comment = models.TextField(default = '')

	timestamp = models.DateField(null = True)

class Conversation(models.Model):

	user1 = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_conversation_user1')
	user2 = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_conversation_user2')


class Message(models.Model):

	conversation_id = models.ForeignKey('Conversation', on_delete = models.CASCADE)
	sender = models.ForeignKey('Users', on_delete = models.CASCADE)

	content = models.TextField(default = '')

	timestamp = models.DateField()

class Notification(models.Model):

	user_sender = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_notification_sender')
	user_receiver = models.ForeignKey('Users', on_delete = models.CASCADE, related_name = 'user_notification_receiver')

	status = models.BooleanField(editable = False, default = False)

	point = models.ForeignKey('Point', on_delete = models.CASCADE)

	timestamp = models.DateField(null = True)












