from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'task', 'deadline', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
