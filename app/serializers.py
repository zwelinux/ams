# serializers.py
from rest_framework import serializers
from .models import Student, Attendance, Subject

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['subject', 'status']

class SubjectAttendanceSerializer(serializers.ModelSerializer):
    average_attendance_rate = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['name', 'average_attendance_rate']

    def get_average_attendance_rate(self, obj):
        student = self.context['student']
        attendances = Attendance.objects.filter(student=student, subject=obj)
        total_records = attendances.count()
        if total_records == 0:
            return 0.0

        present_records = attendances.filter(status='Present').count()
        return (present_records / total_records) * 100

# serializers.py
from rest_framework import serializers
from .models import Student, Attendance, Subject


class StudentSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'subjects']

    def get_subjects(self, obj):
        subjects = Subject.objects.all()
        return SubjectAttendanceSerializer(subjects, many=True, context={'student': obj}).data
    
# serializers.py
from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status']
