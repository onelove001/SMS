from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender = CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin = instance)
        if instance.user_type == 2:
            Staff.objects.create(admin = instance)
        if instance.user_type == 3:
            Student.objects.create(admin = instance, course_id = Course.objects.get(id = 1), session_year_id = Session.objects.get(id = 1),  profile_pic = "", gender = "")


@receiver(post_save, sender = CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()

