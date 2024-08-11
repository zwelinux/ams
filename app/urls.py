# urls.py
from django.urls import path
from .views import AttendanceBySubjectView, AverageAttendanceRateView, StudentSubjectAttendanceView, StudentListView
from .views import attendance_form
from .views import AttendanceCreateView
from django.views.generic import TemplateView
from .views import student_attendance_view

urlpatterns = [
    path('attendance/<str:subject_name>/', AttendanceBySubjectView.as_view(), name='attendance-by-subject'),
    path('attendance/<str:subject_name>/average', AverageAttendanceRateView.as_view(), name='average-attendance-rate'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/attendance/', StudentSubjectAttendanceView.as_view(), name='student-subject-attendance'),
    path('attendance-form/', attendance_form, name='attendance_form'),
    path('attendance-success/', TemplateView.as_view(template_name='attendance_success.html'), name='attendance_success'),
    path('student-attendance/', student_attendance_view, name='student-attendance'),
]
