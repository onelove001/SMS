from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Degree)
admin.site.register(Takes)
admin.site.register(Register)
admin.site.register(Requires)