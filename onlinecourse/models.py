from django.db import models

from onlinecourse_project import settings


class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=False)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENCE = 'data_science'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENCE, 'Data Science'),
        (DATABASE_ADMIN, 'Database Admin'),
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT,
    )

    social_link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.user.username}, {self.occupation}"