from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'author', 'body',)
    list_select_related = True
    #list_filter = ('max_capacity', 'type')
