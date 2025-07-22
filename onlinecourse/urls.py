from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('',view=views.CourseListView.as_view(),name='course_list'),
    path('course/<int:course_id>/enroll/',view=views.enroll,name='enroll'),
    path('course/<int:course_id>',view=views.course_details,name='course_details'),
    path('login/',view=views.login_request,name='login'),
    path('logout/',view=views.logout_request,name='logout'),
    path('registration/',view=views.register_request,name="registration"),

    # Should be created the logic for CRUD Lesson
    # path('lesson/',view=views.lesson_list,name='lesson_list'),
    # path('create_update_lesson',view=views.create_update_lesson,name='create_update_lesson'),
    path('<int:course_id>/submit', view=views.submit, name="submit"),
    # <HINT> Create a route for show_exam_result view
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name="exam_result"),

]