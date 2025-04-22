from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return (obj.title[:10] + '...') if len(obj.title) > 10 else obj.title

    short_title.short_description = "Title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    actions = ['mark_as_done']

    @admin.action(description="Mark selected subtasks as Done")
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status='done')
        self.message_user(request, f"{updated} subtasks marked as done.")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
