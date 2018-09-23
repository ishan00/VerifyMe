from django.db import models
from django.utils import timezone

class Users(models.Model):
	
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

	roll_number = models.CharField(max_length = 30)
	name = models.CharField(max_length = 50)
	department = models.CharField(max_length = 2, choices = LIST_OF_DEPARTMENTS)
	year = models.CharField(max_length = 2,choices = LIST_OF_YEARS)

	privilege = models.BooleanField(editable = False, default = False)
	position = models.CharField(max_length = 100, editable = False, default = '')

	def __str__(self):
		return self.id

class Resume(models.Model):

	user = models.ForeignKey('Users', on_delete = models.CASCADE)
	timestamp = timezone.now()
	status = models.BooleanField(editable = False, default = False)

	def __str__(self):
		return self.id

class Section(models.Model):

	resume_id = models.ForeignKey('Resume', on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)

	def __str__(self):
		return self.id

class Point(models.Model):

	POINT_TYPE = (
		('N','None'),
		('F','Freeze'),
		('P','Pending'),
		('V','Verified'),
		('R','Rejected'),
	)

	resume_id = models.ForeignKey('Resume', on_delete = models.CASCADE)
	section_id = models.ForeignKey('Section', on_delete = models.CASCADE)

	position_in_list = models.IntegerField(editable = False, default = 0)

	point_type = models.CharField(max_length = 1, choices = POINT_TYPE, editable = False, default = 'N')
	user_verify = models.ForeignKey('Users', on_delete = models.CASCADE, null = True)
	point_comment = models.TextField(editable = False, null = True)

	timestamp = models.DateField()

class Request(models.Model):
		




















