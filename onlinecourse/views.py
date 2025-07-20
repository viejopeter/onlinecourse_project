from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from onlinecourse.models import Course, Lesson
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def course_list(request):
    context = {}
    # If request method is POST
    if request.method == 'GET':
        # Using the objects model manage to read all course list
        # and sort them by total_enrollment descending
        course_list = Course.objects.order_by('-total_enrollment')[:10]
        context['course_list'] = course_list
        return render(request, 'onlinecourse/course_list.html', context)
    return None
def enroll(request, course_id):
    # If request method is POST
    if request.method == 'POST':
        # First try to read the course object
        # If could be found, raise a 404 exception
        course = get_object_or_404(Course, pk=course_id)
        # Increase the enrollment by 1
        course.total_enrollment += 1
        course.save()
        # Return a HTTP response redirecting user to course list view
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))
    else:
        return HttpResponse('Inavlid request method', status=405)

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





