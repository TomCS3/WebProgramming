from django.contrib import admin

# Register your models here.
from .models import Post, User, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']
    class meta:
        model = Post

admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Profile)