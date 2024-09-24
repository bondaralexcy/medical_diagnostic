from django.contrib import admin

from users.models import User

# Необходимо зарегистрировать User, иначе не будет видно в Admin

admin.site.register(User)

# Или вот так
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_filter = ("id", "email")
