from django.contrib import admin
from .models import ForumCategory, Thread, Post

@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_pinned', 'is_locked', 'view_count', 'created_at']
    list_filter = ['category', 'is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']