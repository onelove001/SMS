from django.http.response import HttpResponse
from django.shortcuts import *
from django.contrib.auth import login as dlogin, logout, authenticate
from student_management_app.EmailBackend import *
from django.contrib import messages



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

    
