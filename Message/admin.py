from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MessagingGroup)
admin.site.register(UserGroup)
admin.site.register(Message)
admin.site.register(UserMessage)
admin.site.register(GroupMessage)
admin.site.register(Notification)