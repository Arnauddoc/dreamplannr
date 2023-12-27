from django.contrib import admin
from .models import todo, task

admin.site.register(todo)
admin.site.register(task)