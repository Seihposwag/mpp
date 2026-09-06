from django.contrib import admin
from .models import User, Project, Tag, Task, TaskTag


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('owner',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    list_filter = ('owner',)


class TaskTagInline(admin.TabularInline):
    model = TaskTag
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'deadline')
    list_filter = ('status', 'priority', 'user')
    search_fields = ('title', 'description')
    inlines = [TaskTagInline]


@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('task', 'tag', 'created_at')

    