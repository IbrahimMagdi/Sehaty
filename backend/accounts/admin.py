from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserBrowsers)
admin.site.register(CredibilityCodes)
admin.site.register(Emails)
admin.site.register(UserPasswords)
