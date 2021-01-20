"""ProjectSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('courselist/',views.CourseList.as_view()),
    path('courselist/<int:id>/',views.CourseList.as_view()),
    path('batchlist/',views.BatchList.as_view()),
    path('batchlist/<int:id>/',views.BatchList.as_view()),
    path('subjectlist/', views.SubjectList.as_view()),
    path('subjectlist/<int:id>/',views.SubjectList.as_view()),
    path('teacherlist/',views.TeacherList.as_view()),
    path('teacherlist/<int:id>/',views.TeacherList.as_view()),
    path('studentlist/', views.StudentList.as_view()),
    path('student/',views.StudentPage.as_view())

]
