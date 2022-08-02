from django.contrib import admin
from blogapp.models import Profile, UserToken, Category, Post, Comment, SubComment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_image','user','bio')

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('token','user')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    search_fields = ('title',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','add_date')
    search_fields = ('title',)
    list_filter = ('category',)
    list_per_page = 50

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','post','content')

@admin.register(SubComment)
class SubCommentAdmin(admin.ModelAdmin):
    list_display = ('author','post','content','reply')
