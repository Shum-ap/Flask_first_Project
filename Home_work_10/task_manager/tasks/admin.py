
from django.contrib import admin
from .models import Task, SubTask


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1
    fields = ('title', 'description', 'status', 'deadline')
    verbose_name = "Подзадача"
    verbose_name_plural = "Подзадачи"


def mark_as_done(modeladmin, request, queryset):
    updated = queryset.update(status='Done')
    modeladmin.message_user(request, f"{updated} подзадач(и) переведены в статус 'Done'.")
mark_as_done.short_description = "Пометить как Выполнено (Done)"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return obj.title[:10] + "..." if len(obj.title) > 10 else obj.title

    short_title.short_description = "Название"
    short_title.admin_order_field = 'title'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline')
    list_filter = ('status', 'task')
    search_fields = ('title', 'description')
    actions = [mark_as_done]