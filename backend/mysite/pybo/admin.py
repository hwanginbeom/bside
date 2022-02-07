from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(Meet)
admin.site.register(Action)
admin.site.register(Agenda)
admin.site.register(User)
