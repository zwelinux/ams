# views.py
from rest_framework import generics
from .models import Attendance
from .serializers import AttendanceSerializer, StudentSerializer

class AttendanceBySubjectView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        subject_name = self.kwargs['subject_name']
        return Attendance.objects.filter(subject__name=subject_name)

# views.py
from rest_framework import views
from rest_framework.response import Response
from .models import Attendance, Subject, Student
from .serializers import AttendanceSerializer

class AverageAttendanceRateView(views.APIView):
    def get(self, request, subject_name):
        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=404)

        attendances = Attendance.objects.filter(subject=subject)
        total_records = attendances.count()
        if total_records == 0:
            return Response({"average_attendance_rate": 0.0}, status=200)

        present_records = attendances.filter(status='Present').count()
        average_attendance_rate = (present_records / total_records) * 100

        return Response({"average_attendance_rate": average_attendance_rate}, status=200)


# views.py
from rest_framework import views
from rest_framework.response import Response
from .models import Attendance, Subject

class TotalStudentsBySubjectView(views.APIView):
    def get(self, request, subject_name):
        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=404)

        total_students = Attendance.objects.filter(subject=subject).values('student').distinct().count()

        return Response({"total_students": total_students}, status=200)

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentSubjectAttendanceView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# def student_attendance_view(request):
#     students = Student.objects.all()
#     serializer = StudentSerializer(students, many=True)
#     context = {
#         'students': serializer.data
#     }
#     return render(request, 'student_attendance.html', context)

def student_attendance_view(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    
    # Serialize students data
    serializer = StudentSerializer(students, many=True)
    
    context = {
        'students': serializer.data,
        'subjects': subjects
    }
    return render(request, 'student_attendance.html', context)

# views.py
from django.shortcuts import render, redirect
from .forms import AttendanceForm

# def attendance_form(request):
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('attendance_success')
#     else:
#         form = AttendanceForm()
#     return render(request, 'attendance_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Subject
from .forms import AttendanceForm

def attendance_form(request):
    subject_id = request.GET.get('subject_id')
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.subject = subject
            attendance.save()
            return render(request, 'attendance_success.html')
    else:
        form = AttendanceForm()

    return render(request, 'attendance_form.html', {'form': form, 'subject': subject})

# def subject_qr_codes(request):
#     subjects = Subject.objects.all()
#     return render(request, 'subject_qr_codes.html', {'subjects': subjects})

def subject_qr_codes(request):
    subjects = Subject.objects.all()
    qr_code_links = []
    for subject in subjects:
        qr_code_link = f"http://192.168.195.186:8000/media/qr_codes/subject_{subject.id}.png"
        qr_code_links.append({
            'name': subject.name,
            'qr_code_link': qr_code_link
        })
    return render(request, 'subject_qr_codes.html', {'qr_code_links': qr_code_links})


# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
