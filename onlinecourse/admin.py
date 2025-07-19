from django.contrib import admin
from .models import Instructor, Learner, Course, Enrollment, Lesson

# Register your models here.
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Lesson)