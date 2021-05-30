from django.contrib import admin
from .models import Profile, Relationship

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','mobile','email','slug']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Relationship)
