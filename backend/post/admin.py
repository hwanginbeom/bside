from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(Meet)
admin.site.register(User)
admin.site.register(Action)
admin.site.register(Agenda)