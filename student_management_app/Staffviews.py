from django.contrib import messages
import json
from django.http import JsonResponse
from django.shortcuts import *
from .models import *
from django.contrib.postgres.serializers import *
from django.views.decorators.csrf import *


def staff_dashboard(request):
    user = request.user.id
    staff = Staff.objects.get(admin = user)
    subjects = Subject.objects.filter(staff_id = user).count()
    subjectss = Subject.objects.filter(staff_id = user)
    course_id_list = []
    for sub in subjectss:
        course_id = Course.objects.get(id = sub.course_id.id)
        course_id_list.append(course_id.id)

    final_course = []
    for cou in course_id_list:
        if cou not in final_course:
            final_course.append(cou)

    total_studentss = Student.objects.filter(course_id__in = final_course).count()
    # fetch attendance
    attendance_total = Attendance.objects.filter(subject_id__in = subjectss).count()
    staff_leaves = StaffLeaveReport.objects.filter(staff_id = staff).count()

    subject_list = []
    attendance_list = []
    for subject in subjectss:
        attendance_count = Attendance.objects.filter(subject_id = subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count)

    total_students = Student.objects.filter(course_id__in = final_course)
    student_list = []
    student_attendance_list_absent = []
    student_attendance_list_present = []
    for stud in total_students:
        attendance_present = AttendanceReport.objects.filter(student_id = stud.id, status = True).count()
        attendance_absent = AttendanceReport.objects.filter(student_id = stud.id, status = False).count()
        student_attendance_list_absent.append(attendance_absent)
        student_attendance_list_present.append(attendance_present)
        student_list.append(stud.admin.username)

    context = {"student_attendance_list_absent":student_attendance_list_absent, "student_attendance_list_present":student_attendance_list_present, "student_list":student_list, "attendance_list":attendance_list, "subject_list":subject_list, "subjects":subjects, "total_studentss":total_studentss, "attendance_total":attendance_total, "staff_leaves":staff_leaves}
    return render(request, "Stafftemplates/home_content.htm", context)


def staff_take_attendance(request):
    subjects = Subject.objects.filter(staff_id = request.user.id)
    sessions = Session.objects.all()
    context = {
        "subjects":subjects,
        "sessions":sessions,
    }
    return render(request, "Stafftemplates/staff_take_attendance.htm", context)


@csrf_exempt
def get_students(request):
    session = request.POST.get("session_id")
    subject = request.POST.get("subject_id")
 
    session_obj = Session.objects.get(id = session)
    subject_obj = Subject.objects.get(id = subject)

    students = Student.objects.filter(course_id = subject_obj.course_id, session_year_id = session_obj)
    list_data = []
    for student in students:
        data_small = {"id":student.admin.id, "name":student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type = "application/json", safe=False)


@csrf_exempt
def save_attendance(request):
    students = request.POST.get("student_ids")
    attendance = request.POST.get("attendance")
    subject = request.POST.get("subject")
    session = request.POST.get("session")

    subject_obj = Subject.objects.get(id = subject)
    session_obj = Session.objects.get(id = session)
    json_students = json.loads(students)

    try:
        attendance_data = Attendance(subject_id = subject_obj, session_year_id = session_obj, attendance_date = attendance)
        attendance_data.save()

        for stud in json_students:
            stud_obj = Student.objects.get(admin = stud['id'])
            attendance_report = AttendanceReport(student_id = stud_obj, attendance_id = attendance_data, status = stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Failed!")


def staff_update_attendance(request):
    subjects = Subject.objects.filter(staff_id = request.user.id)
    sessions = Session.objects.all()
    context = {"subjects":subjects, "sessions":sessions}
    return render(request, "Stafftemplates/staff_update_attendance.htm", context)


@csrf_exempt
def get_attendance_date(request):
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


@csrf_exempt
def get_attendance_students(request):
    attendance_date = request.POST.get("attendance_date")
    attendance_obj = Attendance.objects.get(id = attendance_date)

    attendance_reports = AttendanceReport.objects.filter(attendance_id = attendance_obj)
    list_data = []

    for student in attendance_reports:
        data = {"id":student.student_id.admin.id, "name":student.student_id.admin.first_name + " " + student.student_id.admin.last_name, "status":student.status}
        list_data.append(data)
    return JsonResponse(json.dumps(list_data), content_type = "application/json", safe = False)


@csrf_exempt
def save_update_attendance_data(request):
    students = request.POST.get("student_ids")
    attendance = request.POST.get("attendance_date")
    attendance_obj = Attendance.objects.get(id = attendance)

    json_students = json.loads(students)

    try:

        for stud in json_students:
            stud_obj = Student.objects.get(admin = stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id = stud_obj, attendance_id = attendance_obj)
            attendance_report.status = stud['status']
            attendance_report.save()
            print(attendance_report)
        return HttpResponse("OK")
    except:
        return HttpResponse("Failed!")


def staff_leave_apply(request):
    staff = Staff.objects.get(admin = request.user.id)
    leave_datas = StaffLeaveReport.objects.filter(staff_id = staff)
    context = {"leave_datas":leave_datas}
    return render(request, "Stafftemplates/staff_leave_apply.htm", context)


def staff_feedback(request):
    staff_obj = Staff.objects.get(admin = request.user.id)
    feedbacks = StaffLeaveFeedback.objects.filter(staff_id = staff_obj)
    context = {"feedbacks":feedbacks}
    return render(request, "Stafftemplates/staff_feedback.htm", context)


def staff_leave_apply_save(request):
    if request.method == "POST":
        date = request.POST.get("leave_date")
        reason = request.POST.get("leave_reason")
        user = Staff.objects.get(admin = request.user.id)
        try:
            staff_report = StaffLeaveReport(staff_id = user, leave_date = date, leave_message = reason)
            staff_report.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))
    return HttpResponse("<h2> Method not Allowed </h2>")


def staff_feedback_save(request):
    if request.method == "POST":
        feedback_message = request.POST.get("staff_feedback")
        # feedback_reply = request.POST.get("staff_feedback_reply")

        user = Staff.objects.get(admin = request.user.id)
        try:
            staff_feed = StaffLeaveFeedback(staff_id = user, feedback = feedback_message, feedback_reply = "")
            staff_feed.save()
            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponse("<h2> Method not ALlowed </h2>")


def staff_profile(request):
    user = Staff.objects.get(admin = request.user.id)
    context = {"user":user}
    return render(request, "Stafftemplates/staff_profile.htm", context)


@csrf_exempt
def staff_fcm_token_save(request):
    token = request.POST.get("token")
    user = request.user.id
    try:
        staff = Staff.objects.get(admin = user)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_profile_save(request): 
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        # password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = Staff.objects.get(admin = user_id)
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


def staff_add_result(request):
    user = request.user.id
    subjects = Subject.objects.filter(staff_id = user)
    sessions = Session.objects.all()
    context = {"subjects":subjects, "sessions":sessions}
    return render(request, "Stafftemplates/staff_add_result.htm", context)


def staff_save_result(request):
    if request.method == "POST":
        student_ids = request.POST.get("student_list")
        ass_mark = request.POST.get("assignment_marks")
        exam_mark = request.POST.get("exam_marks")
        subject = request.POST.get("subject_id")

        student_obj =  Student.objects.get(admin = student_ids)
        subject_obj = Subject.objects.get(id = subject)
        
        try:
            check_exist = StudentResult.objects.filter(subject_id = subject_obj, student_id = student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id = subject_obj, student_id = student_obj)
                result.subject_exam = exam_mark
                result.subject_test = ass_mark
                result.save()
                messages.success(request, "Update Success!")
                return redirect(request.META.get("HTTP_REFERER"))
            result = StudentResult(student_id = student_obj, subject_id = subject_obj, subject_test = ass_mark, subject_exam = exam_mark)
            result.save()

            messages.success(request, "Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))


def edit_student_result(request):
    user = request.user.id
    subjects = Subject.objects.filter(staff_id = user)
    sessions = Session.objects.all()
    context = {"subjects":subjects, "sessions":sessions}
    return render(request, "Stafftemplates/edit_student_result.htm", context)


@csrf_exempt
def fetch_result(request):
    student = request.POST.get("student_idss")
    subject = request.POST.get("subject_id")

    student_obj = Student.objects.get(admin = student)
    subject_obj = Subject.objects.get(id = subject)
   
    try:
        result = StudentResult.objects.filter(student_id = student_obj.id, subject_id = subject_obj).exists()
        if result:
            result = StudentResult.objects.get(student_id = student_obj.id, subject_id = subject_obj)
            result_data = {"exam_mark":result.subject_exam, "ass_mark":result.subject_test}
            
            return HttpResponse(json.dumps(result_data))
        else:
            return HttpResponse("False")

    except:
        return HttpResponse("False")


def edit_student_result_save(request):
     if request.method == "POST":
        student_ids = request.POST.get("student_idss")
        ass_mark = request.POST.get("ass_mark")
        exam_mark = request.POST.get("exam_mark")
        subject = request.POST.get("subject_id")

        student_obj =  Student.objects.get(admin = student_ids)
        subject_obj = Subject.objects.get(id = subject)

        try:
            result = StudentResult.objects.get(subject_id = subject_obj, student_id = student_obj)
            result.subject_exam = exam_mark
            result.subject_test = ass_mark
            result.save()
            messages.success(request, "Update Success!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed!")
            return redirect(request.META.get("HTTP_REFERER"))
