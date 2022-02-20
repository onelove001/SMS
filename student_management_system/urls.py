
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings
from student_management_app.views import *
from student_management_app.HODviews import *
from student_management_app.Studentviews import *
from student_management_app.Staffviews import *

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', login, name = 'login-page'),
    path('login_user', login_user, name = 'login-user'),
    path('logout', logout_user, name = 'logout-user'),

    path('admin_signup', admin_signup, name = 'admin_signup'),
    path('student_signup', student_signup, name = 'student_signup'),
    path('staff_signup', staff_signup, name = 'staff_signup'),

    path('staff_signup_save', staff_signup_save, name = 'staff_signup_save'),
    path('student_signup_save', student_signup_save, name = 'student_signup_save'),
    path('admin_signup_save', admin_signup_save, name = 'admin_signup_save'),

    path('get_user_details', get_user_details, name = 'get-user-details'),
    path('accounts/', include("django.contrib.auth.urls")),



    # Admin urls
    path('admin_dashboard', admin_dashboard, name = 'admin-dashboard'),
    path('add_staff', add_staff, name = 'add-staff'),
    path('add_student', add_student, name = 'add-student'),
    path('add_course', add_course, name = 'add-course'),
    path('add_subject', add_subject, name = 'add-subject'),
    path('add_session', add_session, name = 'add-session'),
    path('add_subject_save', add_subject_save, name = 'add-subject-save'),
    path('add_staff_save', add_staff_save, name = 'add-staff-save'),
    path('add_course_save', add_course_save, name = "add-course-save"),
    path('add_student_save', add_student_save, name = "add-student-save"),
    path('add_session_save', add_session_save, name = "add-session-save"),
    path("manage_staffs", manage_staffs, name = "manage-staffs"),
    path("manage_students", manage_students, name = "manage-students"),
    path("manage_courses", manage_courses, name = "manage-courses"),
    path("manage_subjects", manage_subjects, name = "manage-subjects"),
    path("update_staff/<str:staff_id>", update_staff, name = "update-staff"),
    path("update_student/<str:student_id>", update_student, name = "update-student"),
    path("update_course/<str:course_id>", update_course, name = "update-course"),
    path("update_subject/<str:subject_id>", update_subject, name = "update-subject"),
    path("update_staff_save", update_staff_save, name = "update-staff-save"),
    path("update_student_save", update_student_save, name = "update-student-save"),
    path("update_subject_save", update_subject_save, name = "update-subject-save"),
    path("update_course_save", update_course_save, name = "update-course-save"),
    path("check_email", check_email, name = "check-email"),
    path("check_username", check_username, name = "check-username"),
    path("student_feedback_reply", student_feedback_reply, name = "student-feedback-reply"),
    path("staff_feedback_reply", staff_feedback_reply, name = "staff-feedback-reply"),
    path("staff_feedback_reply_save", staff_feedback_reply_save, name = "staff-feedback-reply-save"),
    path("student_feedback_reply_save", student_feedback_reply_save, name = "student-feedback-reply-save"),
    path("student_leave_view", student_leave_view, name = "student-leave-view"),
    path("student_approve_leave/<str:leave_student_id>", student_approve_leave, name = "student-approve-leave"),
    path("student_disapprove_leave/<str:leave_student_id>", student_disapprove_leave, name = "student-disapprove-leave"),
    path("staff_leave_view", staff_leave_view, name = "staff-leave-view"),
    path("staff_approve_leave/<str:leave_staff_id>", staff_approve_leave, name = "staff-approve-leave"),
    path("staff_disapprove_leave/<str:leave_staff_id>", staff_disapprove_leave, name = "staff-disapprove-leave"),
    path("admin_view_attendance", admin_view_attendance, name = "admin-view-attendance"),
    path("admin_get_attendance_date", admin_get_attendance_date, name = "admin-get-attendance-date"),
    path("admin_get_attendance_students", admin_get_attendance_students, name = "admin-get-attendance-students"),
    path("admin_profile", admin_profile, name = "admin-profile"),
    path("admin_profile_save", admin_profile_save, name = "admin-profile-save"),


    
    # Staff Urls
    path("staff_dashboard", staff_dashboard, name = "staff-dashboard"),
    path("staff_take_attendance", staff_take_attendance, name = "staff-take-attendance"),
    path("get_students", get_students, name = "get-students"),
    path("save_attendance", save_attendance, name = "save-attendance"),
    path("staff_update_attendance", staff_update_attendance, name = "staff-update-attendance"),
    path("get_attendance_date", get_attendance_date, name = "get-attendance-date"),
    path("get_attendance_students", get_attendance_students, name = "get-attendance-students"),
    path("save_update_attendance_data", save_update_attendance_data, name = "save-update-attendance-data"),
    path("staff_feedback", staff_feedback, name = "staff-feedback"),
    path("staff_leave_apply", staff_leave_apply, name = "staff-apply-leave"),
    path("staff_leave_apply_save", staff_leave_apply_save, name = "staff-apply-leave-save"),
    path("staff_feedback_save", staff_feedback_save, name = "staff-feedback-save"),
    path("staff_profile", staff_profile, name = "staff-profile"),
    path("staff_profile_save", staff_profile_save, name = "staff-profile-save"),
    path("staff_fcm_token_save", staff_fcm_token_save, name = "staff_fcm_token_save"),
    path("staff_add_result", staff_add_result, name = "staff_add_result"),
    path("staff_save_result", staff_save_result, name = "staff_save_result"),
    path("edit_student_result", edit_student_result, name = "edit_student_result"),
    path("edit_student_result_save", edit_student_result_save, name = "edit_student_result_save"),
    path("fetch_result", fetch_result, name = "fetch_result"),
    


    # student urls 
    path("student_dashboard", student_dashboard, name = "student-dashboard"),
    path("student_view_attendance", student_view_attendance, name = "student-view-attendance"),
    path("student_view_attendance_post", student_view_attendance_post, name = "student-view-attendance-post"),
    path("student_feedback", student_feedback, name = "student-feedback"),
    path("student_leave_apply", student_leave_apply, name = "student-apply-leave"),
    path("student_leave_apply_save", student_leave_apply_save, name = "student-apply-leave-save"),
    path("student_feedback_save", student_feedback_save, name = "student-feedback-save"),
    path("student_profile", student_profile, name = "student-profile"),
    path("student_profile_save", student_profile_save, name = "student-profile-save"),
    path("student_fcm_token_save", student_fcm_token_save, name = "student_fcm_token_save"),
    path("student_view_result", student_view_result, name = "student_view_result"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
