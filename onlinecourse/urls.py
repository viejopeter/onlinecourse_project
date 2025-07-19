from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('',view=views.course_list,name='course_list'),
    path('course/<int:course_id>/enroll/',view=views.enroll,name='enroll'),
    path('course/<int:course_id>',view=views.course_details,name='course_details'),
]