from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    immigrant = models.BooleanField(default=False)
    identify_as = models.CharField(max_length=255, blank=True, null=True)
    country_state = models.CharField(max_length=255, blank=True, null=True)
    originally_from = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    language_preference = models.CharField(max_length=255, blank=True, null=True)
    interest = models.CharField(max_length=255, blank=True, null=True)
    preferred_coaching_style = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    language_preference = models.CharField(max_length=255, blank=True, null=True)
    countries = models.CharField(max_length=255, blank=True, null=True)
    previous_countries = models.CharField(max_length=255, blank=True, null=True)
    identity = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    forte_strength = models.CharField(max_length=255, blank=True, null=True)
    coaching_style = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(default=0)
    client_preference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class UserMentorMatch(models.Model):
    TYPE_CHOICE = [('mentor', 'Mentor'), ('student', 'Student')]
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=TYPE_CHOICE, max_length=10)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} : {self.status}"


# ==============================signals to create user profiles automatically ================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        if instance.is_mentor:
            MentorProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_student:
        instance.student_profile.save()
    if instance.is_mentor:
        instance.mentor_profile.save()
