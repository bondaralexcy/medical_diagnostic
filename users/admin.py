from django.contrib import admin

from users.models import User

# Register your models here.
# Необходимо зарегистрировать User, иначе не будет видно в Admin

admin.site.register(User)

#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
    #list_display = ['pk', 'email', 'first_name', 'is_active', 'is_staff', 'is_superuser']
