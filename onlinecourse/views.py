from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic

from onlinecourse.models import Course, Lesson, Enrollment, Submission
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:course_list')
        else:
            context['message'] = 'Invalid username or password.'
            return render(request,'onlinecourse/user_login.html',context)

    else:
       return render(request,"onlinecourse/user_login.html")

def logout_request(request):
    print(" User {} logged out".format(request.user.username))
    logout(request)
    return redirect("onlinecourse:course_list")

def register_request(request):
    context = {}
    if request.method == 'GET':

        return render(request, "onlinecourse/user_registration.html")

    elif request.method == 'POST':

        username = request.POST['username']
        password = request.POST['psw']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user_exist= False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("User does not exist")


        if not user_exist:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            login(request, user)
            return redirect('onlinecourse:course_list')
        else:
            context['message'] = 'User already exists.'
            return render(request,'onlinecourse/user_registration.html',context)

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses

def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled

def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

def course_details(request, course_id):
    context = {}
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            context['course'] = course
            # Use render() method to generate HTML page by combining
            # template and context
            return render(request, 'onlinecourse/course_detail.html', context)
        except Course.DoesNotExist:
            # If course does not exist, throw a Http404 error
            raise Http404("No course matches the given id.")

def lesson_list(request):
    context = {}
    if request.method == 'GET':
        list_all_lessons = Lesson.objects.all()
        context['lesson_list'] = list_all_lessons
        return render(request,"onlinecourse/lesson_list.html",context)
def create_update_lesson(request):
    context ={}
    if request.method == 'GET':
        courses_list = Course.objects.all()
        context['courses_list'] = courses_list
        return render(request,"onlinecourse/crud_lesson.html",context)
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        last_lesson = Lesson.objects.order_by('-order').first()
        order = last_lesson.order + 1 if last_lesson is not None else 1
        course_id = request.POST['course']
        course = get_object_or_404(Course, pk=course_id)
        Lesson.objects.create(title=title, content=content, order=order, course=course)
        lesson_list = Lesson.objects.all()
        context['lesson_list'] = lesson_list
        return render(request,"onlinecourse/lesson_list.html",context)


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    submission_id = submission.id
    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course_id, submission_id,)))


def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
    return submitted_anwsers


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    total_score = 0
    questions = course.question_set.all()

    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)
        selected_choices = choices.filter(question=question)

        if set(correct_choices) == set(selected_choices):
            total_score += question.grade

    context['course'] = course
    context['grade'] = total_score
    context['choices'] = choices

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)





