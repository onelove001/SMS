from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import *
from django.urls import *


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user = request.user
        
        if user.is_authenticated:

            if user.user_type == "1":
                if modulename == "student_management_app.HODviews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin-dashboard")

            elif user.user_type == "2":
                if modulename == "student_management_app.Staffviews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("staff-dashboard")

            elif user.user_type == "3": 
                if modulename == "student_management_app.Studentviews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("student-dashboard")
            else:
                return redirect("login-page")

        else:
            if request.path == reverse("login-page") or request.path == reverse("login-user") or modulename == "django.contrib.auth.views" or modulename == "student_management_app.views":
                pass

            else:
                return redirect("login-page")

