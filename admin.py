from django.contrib import admin
from .models import Teacher, Student, Batch,Academicyear,Course,Fee,Category,Subcategory,Transport,Assign,Busdetails,Busstop
from.models import Busroute
from .models import Teacher, Student, Batch,Academicyear,Course,Timetable,Order
from . import  models

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Batch)
admin.site.register(Academicyear)
admin.site.register(Course)
admin.site.register(Timetable)
admin.site.register(models.AttendanceMarked)
admin.site.register(Order)
admin.site.register(models.Attendance)
admin.site.register(Fee)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Transport)
admin.site.register(Assign)
admin.site.register(Busdetails)
admin.site.register(Busstop)
admin.site.register(Busroute)
admin.site.register(models.Placement)
admin.site.register(models.Quata)
admin.site.register(models.PlacementBulk)
admin.site.register(models.HigherStudies)