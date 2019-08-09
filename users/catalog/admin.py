from django.contrib import admin

# Register your models here.
from catalog.models import User

#admin.site.register(User)

class UserAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'username', 'email')

admin.site.register(User, UserAdmin)