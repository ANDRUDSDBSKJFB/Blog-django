from django.contrib import admin
from .models import Post, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('owner',  'body')


admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'owner', 'created')


admin.site.register(Post, PostAdmin)