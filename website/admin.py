from django.contrib import admin
from .models import Users,Resume,Section,Point,Request,Conversation,Message,Notification,Passwords

admin.site.register(Users)
admin.site.register(Resume)
admin.site.register(Section)
admin.site.register(Point)
admin.site.register(Request)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Passwords)