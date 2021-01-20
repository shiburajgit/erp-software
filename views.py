from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,pagination
from school import models

class CourseList(APIView):
    def get(self, request,id=None):
        if id == None:
            course=models.Course.objects.all()
            serializer=serializers.CourseSerializer(course, many=True)

        else:
            course = models.Batch.objects.get(id=id)
            serializer=serializers.CourseSerializer(course)
        return Response(serializer.data)

class BatchList(APIView):
    def get(self, request):
        batch=models.Batch.objects.filter(academicid__isactive =True)
        serializer=serializers.BatchSerializer(batch, many=True)
        return Response(serializer.data)

class SubjectList(APIView):
    def get(self, request):
        subject=models.Subject.objects.filter(academicid__isactive =True)
        serializer=serializers.SubjectSerializer(subject, many=True)
        return Response(serializer.data)

class TeacherList(APIView):
    def get(self, request):
        teacher=models.AssignTeacher.objects.all()
        serializer=serializers.AssignTeacherSerializer(teacher,many=True)
        return Response(serializer.data)

class StudentList(APIView):
    def get(self, request):
        student=models.Student.objects.all()
        serializer=serializers.StudentSerializer(student,many=True)
        return Response(serializer.data)

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self,data):
        return Response({
            'link':{
                'next':self.get_next_link(),
                'previous':self.get_next_link(),
            },
            'count':self.page.paginator.count,
            'results':data
        })


class StudentPage(APIView):
    def get(self, request):
        data = models.Student.objects.all()
        # paginator = pagination.PageNumberPagination
        paginator = CustomPagination()
        paginator.page_size = 100
        result_page = paginator.paginate_queryset(data, request)
        student = serializers.StudentSerializer(result_page,many=True)
        if student.is_valid:
            return paginator.get_paginated_response(student.data)
        else:
            msg = False
            error = student.errors
            statuss = status.HTTP_400_BAD_REQUEST
            return Response({'success':msg, 'error':error,'status':statuss})
