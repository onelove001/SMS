from email import message
from multiprocessing import context
import re
from django.http.response import HttpResponse
from django.shortcuts import *
from student_management_app.EmailBackend import *
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import *
from django.http import JsonResponse
import json



def admin_dashboard(request):
    staff_count = Staff.objects.all().count()
    student_count = Student.objects.all().count()
    subject_count = Subject.objects.all().count()
    course_count = Course.objects.all().count()
    subject_list = []
    course_list_name = []

    courses = Course.objects.all()
    for course in courses:
        subjects = Subject.objects.filter(course_id = course.id).count()
        subject_list.append(subjects)
        course_list_name.append(course.course_name)

    student_list = []
    course_list = []
    for course in courses:
        students = Student.objects.filter(course_id = course.id).count()
        student_list.append(students)
        course_list.append(course.course_name)

    subjectss = Subject.objects.all()
    student_list_subject = []
    subject_list_names = []

    for subje in subjectss:
        studentsss = Student.objects.filter(course_id = subje.course_id).count()
        student_list_subject.append(studentsss)
        subject_list_names.append(subje.subject_name)

    staffs = Staff.objects.all()
    attendance_present_staff = []
    attendance_absent_staff = []
    staff_names = []
    for staff in staffs:
        subjectssss = Subject.objects.filter(staff_id = staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in = subjectssss).count()
        attendance_present_staff.append(attendance)
        leaves = StaffLeaveReport.objects.filter(staff_id = staff.id, leave_status = 1).count()
        attendance_absent_staff.append(leaves)
        staff_names.append(staff.admin.username)

    studentsss = Student.objects.all()
    attendance_present_students = []
    attendance_absent_students = []
    student_names = []
    for stu in studentsss:
        attendance = AttendanceReport.objects.filter(student_id = stu.id, status = True).count()
        attendance_abs = AttendanceReport.objects.filter(student_id = stu.id, status = False).count()
        leaves = StudentLeaveReport.objects.filter(student_id = stu.id, leave_status = 1).count()
        attendance_present_students.append(attendance)
        attendance_absent_students.append(leaves+attendance_abs)
        student_names.append(stu.admin.username)

  
    context = {"attendance_present_students":attendance_present_students, "attendance_absent_students":attendance_absent_students, "student_names":student_names, "staff_names":staff_names, "attendance_absent_staff":attendance_absent_staff, "attendance_present_staff":attendance_present_staff, "subject_list_names":subject_list_names, "student_list_subject":student_list_subject, "student_list":student_list, "course_list":course_list, "subject_list":subject_list, "course_list_name":course_list_name, "staff_count":staff_count, "student_count":student_count, "subject_count":subject_count, "course_count":course_count}
    return render(request, "HODtemplates/home_content.htm", context)


def add_staff(request):
    return render(request, "HODtemplates/add_staff.htm", {})


def add_course(request):
    return render(request, "HODtemplates/add_course.htm", {})


def add_subject(request):
    staffs = CustomUser.objects.filter(user_type = 2)
    courses = Course.objects.all()
    context = {"staffs":staffs, "courses":courses}
    return render(request, "HODtemplates/add_subject.htm", context)


def add_student(request):
    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {
        "courses":courses,
        "sessions":sessions,
    }
    return render(request, "HODtemplates/add_student.htm", context)


def add_session(request):
    context = {}
    return render(request, "HODtemplates/add_session.htm", context)


def add_staff_save(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.create_user(email = email, username = username, first_name = first_name, last_name = last_name, password = password, user_type = 2)
            user.staff.address = address
            user.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))
    return HttpResponse("<h2> Method Not Allowed </h2>")


def add_course_save(request):
    if request.method == "POST":
        course = request.POST.get('course')

        try:
            course_obj = Course(course_name = course)
            course_obj.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))


def add_subject_save(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        staff_id = request.POST.get("staff_id")
        subject = request.POST.get("subject")
        course_obj = Course.objects.get(id = course_id)
        staff_obj = CustomUser.objects.get(id = staff_id)
        try:
            sub_obj = Subject(course_id = course_obj, staff_id = staff_obj, subject_name = subject)
            sub_obj.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))


def add_student_save(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        course_id = request.POST.get("course_id")
        gender = request.POST.get("gender")
        session_id = request.POST.get("session_id")
        session_obj = Session.objects.get(id = session_id)

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        password = request.POST.get("password")
        course_obj = Course.objects.get(id = course_id)

        try:
            user = CustomUser.objects.create_user(email = email, username = username, first_name = first_name, last_name = last_name, password = password, user_type = 3)
            user.student.address = address
            user.student.course_id = course_obj
            user.student.session_year_id = session_obj
            user.student.course_id = course_obj
            user.student.gender = gender
            user.student.profile_pic = profile_pic_url
            user.save()

            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))
    return HttpResponse("<h2> Method Not Allowed </h2>")


def add_session_save(request):
    if request.method == "POST":
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        
        try: 
            session = Session(session_start_year = session_start, session_end_year = session_end)
            session.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))


def manage_staffs(request):
    staffs = Staff.objects.all()
    context = {"staffs":staffs}
    return render(request, "HODtemplates/manage_staff.htm", context)


def manage_students(request):
    students = Student.objects.all()
    context = {"students":students}
    return render(request, "HODtemplates/manage_student.htm", context)


def manage_courses(request):
    courses = Course.objects.all()
    context = {"courses":courses}
    return render(request, "HODtemplates/manage_course.htm", context)


def manage_subjects(request):
    subjects = Subject.objects.all()
    context = {"subjects":subjects}
    return render(request, "HODtemplates/manage_subject.htm", context)


def update_staff(request, staff_id):
    staff = Staff.objects.get(admin = staff_id)
    context = {"staff":staff, "id":staff_id}
    return render(request, "HODtemplates/update_staff.htm", context)


def update_student(request, student_id):
    student = Student.objects.get(admin = student_id)
    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {"student":student, "courses":courses, "id":student_id, "sessions":sessions}
    return render(request, "HODtemplates/update_student.htm", context)


def update_course(request, course_id):
    course = Course.objects.get(id = course_id)
    context = {"course":course, "id":course_id}
    return render(request, "HODtemplates/update_course.htm", context)


def update_subject(request, subject_id):
    subject = Subject.objects.get(id = subject_id)
    courses = Course.objects.all()
    staffs = Staff.objects.all()
    context = {"subject":subject, "courses":courses, "staffs":staffs, "id":subject_id}
    return render(request, "HODtemplates/update_subject.htm", context)


def update_staff_save(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        staff_id = request.POST.get("staff_id")
        
        try:
            staff_user = CustomUser.objects.get(id = staff_id)
            
            staff_user.email = email
            staff_user.first_name = first_name
            staff_user.last_name = last_name
            staff_user.username = username
            staff_user.save()

            staff_obj = Staff.objects.get(admin = staff_id)
            staff_obj.address = address
            staff_obj.save()
            
            
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("<h2> Method not allowed </h2> ")


def update_student_save(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("course_id")
        session_id = request.POST.get("session_id")
        student_id = request.POST.get("student_id")
        session_obj = Session.objects.get(id = session_id)

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        
        try:
            student_user = CustomUser.objects.get(id = student_id)
            course_obj = Course.objects.get(id = course_id)
            student_user.email = email
            student_user.first_name = first_name
            student_user.last_name = last_name
            student_user.username = username
            student_user.save()
            
            student_obj = Student.objects.get(admin = student_id)
            student_obj.address = address
            student_obj.gender = gender
            student_obj.course_id = course_obj
            student_obj.session_year_id = session_obj
            if profile_pic_url is not None:
                student_obj.profile_pic = profile_pic_url
            student_obj.save()

            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("<h2> Method not allowed </h2> ")


def update_subject_save(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course_id")
        staff_id = request.POST.get("staff_id")

        course_obj = Course.objects.get(id = course_id)
        staff_obj = CustomUser.objects.get(id = staff_id)

        try:
            subject = Subject.objects.get(id = subject_id)
            subject.subject_name = subject_name
            subject.course_id = course_obj
            subject.staff_id = staff_obj
            subject.save()

            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))


def update_course_save(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")

        try:
            course = Course.objects.get(id = course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))


@csrf_exempt
def check_email(request):
    email = request.POST.get("email")
    user = CustomUser.objects.filter(email = email)
    if user:
        return HttpResponse(True)
    return HttpResponse(False)


@csrf_exempt
def check_username(request):
    username = request.POST.get("username")
    user = CustomUser.objects.filter(username = username)
    if user:
        return HttpResponse(True)
    return HttpResponse(False)


def student_feedback_reply(request):
    feedbacks = StudentLeaveFeedback.objects.all()
    context = {"feedbacks":feedbacks}
    return render(request, "HODtemplates/student_feedback_reply.htm", context)


def staff_feedback_reply(request):
    feedbacks = StaffLeaveFeedback.objects.all()
    context = {"feedbacks":feedbacks}
    return render(request, "HODtemplates/staff_feedback_reply.htm", context)


@csrf_exempt
def student_feedback_reply_save(request):
    message_reply = request.POST.get("reply_message")
    feedback_id = request.POST.get("feedback_id")
    try:
        feedback = StudentLeaveFeedback.objects.get(id = feedback_id)
        feedback.fieldback_reply = message_reply
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_reply_save(request):
    message_reply = request.POST.get("reply_message")
    feedback_id = request.POST.get("feedback_id")
    try:
        feedback = StaffLeaveFeedback.objects.get(id = feedback_id)
        feedback.feedback_reply = message_reply
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_leave_view(request):
    leaves = StaffLeaveReport.objects.all()
    context = {"leaves":leaves}
    return render(request, "HODtemplates/staff_leave_view.htm", context)


def staff_approve_leave(request, leave_staff_id):
    leave = StaffLeaveReport.objects.get(id = leave_staff_id)
    leave.leave_status = 1
    leave.save()
    return redirect(request.META.get("HTTP_REFERER"))


def staff_disapprove_leave(request, leave_staff_id):
    leave = StaffLeaveReport.objects.get(id = leave_staff_id)
    leave.leave_status = 0
    leave.save()
    return redirect(request.META.get("HTTP_REFERER"))


def student_leave_view(request):
    leaves = StudentLeaveReport.objects.all()
    context = {"leaves":leaves}
    return render(request, "HODtemplates/student_leave_view.htm", context)


def student_approve_leave(request, leave_student_id):
    leave = StudentLeaveReport.objects.get(id = leave_student_id)
    leave.leave_status = 1
    leave.save()
    return redirect(request.META.get("HTTP_REFERER"))


def student_disapprove_leave(request, leave_student_id):
    leave = StudentLeaveReport.objects.get(id = leave_student_id)
    leave.leave_status = 0
    leave.save()
    return redirect(request.META.get("HTTP_REFERER"))


@csrf_exempt
def admin_get_attendance_students(request):
    attendance_date = request.POST.get("attendance_date")
    attendance_obj = Attendance.objects.get(id = attendance_date)

    attendance_reports = AttendanceReport.objects.filter(attendance_id = attendance_obj)
    list_data = []

    for student in attendance_reports:
        data = {"id":student.student_id.admin.id, "name":student.student_id.admin.first_name + " " + student.student_id.admin.last_name, "status":student.status}
        list_data.append(data)
    return JsonResponse(json.dumps(list_data), content_type = "application/json", safe = False)


@csrf_exempt
def admin_get_attendance_date(request):
    subject = request.POST.get("subject_id")
    session = request.POST.get("session_id")

    subject_iddd = Subject.objects.get(id = subject)
    session_iddd = Session.objects.get(id = session)

    attendances = Attendance.objects.filter(subject_id = subject_iddd, session_year_id = session_iddd)
    attendance_list = []
    for attendance in attendances:
        attendance_data = {"id":attendance.id, "attendance_date":str(attendance.attendance_date), "subject_id":attendance.subject_id.id, "session_year_id":attendance.session_year_id.id}
        attendance_list.append(attendance_data)

    return JsonResponse(json.dumps(attendance_list), safe=False)


def admin_view_attendance(request):
    subjects = Subject.objects.all()
    sessions = Session.objects.all()
    context = {"subjects":subjects, "sessions":sessions}
    return render(request, "HODtemplates/admin_view_attendance.htm", context)


def admin_profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {"user":user}
    return render(request, "HODtemplates/admin_profile.htm", context)


def admin_profile_save(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        try:

            user = CustomUser.objects.get(id = user_id)
            user.first_name = firstname
            user.last_name = lastname
            if password != None and password != "":
               user.set_password(password)
            user.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))