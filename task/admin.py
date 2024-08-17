from django.contrib import admin
from .models import Task
# Register your models here.
class TaskCreated(admin.ModelAdmin):
    readonly_fields = ("created",)

admin.site.register(Task, TaskCreated)