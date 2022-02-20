from django.http.response import HttpResponse
from django.shortcuts import *
from django.contrib.auth import login as dlogin, logout, authenticate
from student_management_app.EmailBackend import *
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from student_management_app.models import CustomUser



def login(request):
    return render(request, "login.htm", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = EmailBackend.authenticate(request, username, password)
        if user is not None:
            dlogin(request, user)
            if user.user_type == "1":
                return redirect("admin-dashboard")
            elif user.user_type == "2":
                return redirect("staff-dashboard")
            elif user.user_type == "3":
                return redirect("student-dashboard")
        else:
            messages.error(request, "Invalid Login Details! ")
            return redirect("login-page")
    
    messages.error(request, "Method Not Allowed")
    return redirect("login-page")


def logout_user(request):
    logout(request)
    return redirect("login-page")


def get_user_details(request):
    if request.user is not None:
        return HttpResponse("username: " + request.user.email + "user type: " + request.user.user_type)
    return HttpResponse(" Please Login First ")

    
def admin_signup(request):
    context = {}
    return render(request, "admin_signup.htm", context)


def admin_signup_save(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.create_user(username = username, email = email, password = password, user_type = 1)
            user.save()
            messages.success(request, "Admin Account Created!")
            return redirect("login-page")
        except:
            messages.error(request, "Admin Account Failed!")
            return redirect("login-page")


def staff_signup(request):
    context = {}
    return render(request, "staff_signup.htm", context)


def staff_signup_save(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username = username, email = email, password = password, user_type = 2)
            user.staff.address = address
            user.save()
            messages.success(request, "Staff Account Created!")
            return redirect("login-page")
        except:
            messages.error(request, "Staff Account Failed!")
            return redirect("login-page")



def student_signup(request):
    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {"courses":courses, "sessions":sessions}
    return render(request, "student_signup.htm", context)



def student_signup_save(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        lastname = request.POST.get("lastname")
        firstname = request.POST.get("firstname")
        course = request.POST.get("course_id")
        gender = request.POST.get("gender")
        session = request.POST.get("session_id")

        course_obj = Course.objects.get(id = course)
        session_obj = Session.objects.get(id = session)

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(username = username, last_name = lastname, first_name = firstname, email = email, password = password, user_type = 3)
            user.student.address = address
            user.student.gender = gender
            user.student.course_id = course_obj
            user.student.session_year_id = session_obj
            user.student.profile_pic = profile_pic_url
            user.save()

            messages.success(request, "Student Account Created!")
            return redirect("login-page")

        except:
            messages.error(request, "Student Account Failed!")
            return redirect("login-page")

