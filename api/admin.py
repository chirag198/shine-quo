from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, MentorProfile, UserMentorMatch


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_mentor')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(MentorProfile)
admin.site.register(UserMentorMatch)
