from rest_framework import serializers
from school import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course

        # fields = ['ename']

        fields = '__all__'
        depth =1

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Batch

        # fields = ['ename']

        fields = '__all__'
        depth =1
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject

        # fields = ['ename']

        fields = '__all__'
        depth =1

class AssignTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssignTeacher
        fields = '__all__'
        depth =1

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'
        depth = 1
