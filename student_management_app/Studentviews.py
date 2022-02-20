from django.shortcuts import *
from .models import *
import datetime
from django.contrib import messages
from django.views.decorators.csrf import *




def student_dashboard(request):
    student_obj = Student.objects.get(admin = request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id = student_obj).count()
    attendance_total_present = AttendanceReport.objects.filter(student_id = student_obj, status = 1).count()
    attendance_total_absent = AttendanceReport.objects.filter(student_id = student_obj, status = 0).count()
    course = Course.objects.filter(id = student_obj.course_id.id).first()
    subjects = Subject.objects.filter(course_id = course).count()

    subject_name = []
    data_present = []
    data_absent = []
    
    subjectss = Subject.objects.filter(course_id = student_obj.course_id)
    for sub in subjectss:
        attendance = Attendance.objects.filter(subject_id = sub.id)
        attendance_report_present = AttendanceReport.objects.filter(attendance_id__in = attendance, status = True, student_id = student_obj.id).count()
        attendance_report_absent = AttendanceReport.objects.filter(attendance_id__in = attendance, status = False, student_id = student_obj.id).count()
        subject_name.append(sub.subject_name)
        data_present.append(attendance_report_present)
        data_absent.append(attendance_report_absent)

    context = {"subject_name":subject_name, "data_present":data_present, "data_absent":data_absent, "subjects":subjects, "attendance_total":attendance_total, "attendance_total_present":attendance_total_present, "attendance_total_absent":attendance_total_absent}
    return render(request, "Studenttemplates/home_content.htm", context)


def student_view_attendance(request):
    student = Student.objects.get(admin = request.user.id)
    course_obj = Course.objects.get(id = student.course_id.id)
    subjects = Subject.objects.filter(course_id = course_obj)
    context = {"subjects":subjects}
    return render(request, "Studenttemplates/student_view_attendance.htm", context)


def student_view_attendance_post(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        subject = request.POST.get("subject_id")

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        subject_obj = Subject.objects.get(id = subject)
        student = Student.objects.get(admin = request.user.id)

        attendance = Attendance.objects.filter(attendance_date__range=(start_date, end_date), subject_id = subject_obj)
        attendance_reps = AttendanceReport.objects.filter(attendance_id__in = attendance, student_id = student)

    context = {"attendance_reps":attendance_reps}
    return render(request, "Studenttemplates/student_attendance_data.htm", context)


def student_leave_apply(request):
    student = Student.objects.get(admin = request.user.id)
    leave_datas = StudentLeaveReport.objects.filter(student_id = student)
    context = {"leave_datas":leave_datas}
    return render(request, "Studenttemplates/student_leave_apply.htm", context)


def student_feedback(request):
    student_obj = Student.objects.get(admin = request.user.id)
    feedbacks = StudentLeaveFeedback.objects.filter(student_id = student_obj)
    context = {"feedbacks":feedbacks}
    return render(request, "Studenttemplates/student_feedback.htm", context)


def student_leave_apply_save(request):
    if request.method == "POST":
        date = request.POST.get("leave_date")
        reason = request.POST.get("leave_reason")
        user = Student.objects.get(admin = request.user.id)
        try:
            student_report = StudentLeaveReport(student_id = user, leave_date = date, leave_message = reason)
            student_report.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))
    return HttpResponse("<h2> Method not Allowed </h2>")


def student_feedback_save(request):
    if request.method == "POST":
        feedback_message = request.POST.get("student_feedback")
        # feedback_reply = request.POST.get("staff_feedback_reply")

        user = Student.objects.get(admin = request.user.id)
        try:
            student_feed = StudentLeaveFeedback(student_id = user, fieldback = feedback_message, fieldback_reply = "")
            student_feed.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("<h2> Method not ALlowed </h2>")


def student_profile(request):
    user = Student.objects.get(admin = request.user.id)
    context = {"user":user}
    return render(request, "Studenttemplates/student_profile.htm", context)


@csrf_exempt
def student_fcm_token_save(request):
    token = request.POST.get("token")
    user = request.user.id
    try:
        student = Student.objects.get(admin = user)
        student.fcm_token = token
        student.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)


def student_profile_save(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        address = request.POST.get("address")
        
        # password = request.POST.get("password")
        try:

            user = Student.objects.get(admin = user_id)
            user_custom = CustomUser.objects.get(id = user_id)
            user_custom.first_name = firstname
            user_custom.last_name = lastname
            user.address = address
            # if password != None and password != "":
            #    user_custom.set_password(password)
            user_custom.save()
            user.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))

        
def student_view_result(request):
    user = request.user.id
    student_obj = Student.objects.get(admin = user)
    my_results = StudentResult.objects.filter(student_id = student_obj.id)
    context = {"my_results":my_results}
    return render(request, "Studenttemplates/student_view_result.htm", context)