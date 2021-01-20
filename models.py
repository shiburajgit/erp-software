from django.db import models
from django.contrib.auth.models import AbstractUser
import os



# Create your models here.
# class User(AbstractUser):
#     studclass=models.IntegerField(null=True, blank=True)
#     fine=models.IntegerField(null=True, blank=True)
from django.db.models import CharField


class Academicyear(models.Model):
    academicyearname=models.CharField(max_length=255, null=True, blank=True)
    startson=models.DateField(null=True,blank=True)
    endson=models.DateField(null=True,blank=True)
    addondate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    isactive = models.BooleanField(default=False, null=True, blank=True)

class Quata(models.Model):
    AdmittedQuata = models.CharField(max_length=255)


class Course(models.Model):
    coursename=models.CharField(max_length=255)
    code=models.CharField(max_length=255, null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    isactive=models.BooleanField(default=True, null=True,blank=True)
    addondate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    academicid=models.ForeignKey(Academicyear,on_delete=models.CASCADE)

    def __int__(self):
        return self.academicid

class Batch(models.Model):
    batchname=models.CharField(max_length=255)
    courseid=models.ForeignKey(Course, on_delete=models.CASCADE)
    addondate = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updateddate = models.DateTimeField(auto_now=True,null=True, blank=True)
    academicid = models.ForeignKey(Academicyear,null=True, blank=True, on_delete=models.CASCADE)


class Student(models.Model):
    AdmissionNumber=models.IntegerField(blank=True,null=True)
    AdmissionYear=models.CharField(max_length=255,null=True,blank=True)
    FirstName=models.CharField(max_length=255)
    LastName=models.CharField(max_length=255,null=True,blank=True)
    Email=models.CharField(max_length=255,null=True,blank=True)
    DOB=models.DateField()
    BloodGroup=models.CharField(max_length=255, null=True, blank=True)
    PhoneNumber=models.CharField(max_length=255,null=True,blank=True)
    ContactDetails=models.CharField(max_length=255,null=True,blank=True)
    Gender=models.CharField(max_length=255)
    RollNo=models.IntegerField(null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    Batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=True,blank=True)
    academicyear=models.ForeignKey(Academicyear,on_delete=models.CASCADE,null=True,blank=True)
    attend=models.CharField(max_length=255, null=True, blank=True)
    AdmittedQuata=models.ForeignKey(Quata,on_delete=models.CASCADE,null=True,blank=True)


class Book(models.Model):
    BookName=models.CharField(max_length=255,null=True,blank=True)
    AuthorName=models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True,blank=True)
    Number=models.IntegerField()
    TotalCount=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.BookName


class Teacher(models.Model):
    Name=models.CharField(max_length=255)
    Designation=models.CharField(max_length=255)
    Education=models.CharField(max_length=255)
    Experiance=models.IntegerField()
    Gender=models.CharField(max_length=255)
    Subject=models.CharField(max_length=255, null=True, blank=True)


class Order(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    BookName = models.ForeignKey(Book, on_delete=models.CASCADE)
    issuedate = models.DateField(null=True,blank=True,auto_now_add=True)
    returndate = models.DateField(null=True,blank=True)
    duedate=models.DateField(null=True, blank=True)
    fine=models.IntegerField(null=True,blank=True)


class Bloodgroup(models.Model):
    group = models.CharField(max_length=255)
    studentid=models.ForeignKey(Student, on_delete=models.CASCADE)
    addondate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)

class Subject(models.Model):
    subject=models.CharField(max_length=255)
    academicid=models.ForeignKey( Academicyear,on_delete=models.CASCADE,null=True,blank=True,)
    courseid=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True,)
    syllabus= models.FileField(upload_to="syllabus/", null=True, blank=True)


class Timetable(models.Model):
    Day=models.CharField(null=True, blank=True, max_length=255)
    starttime=models.CharField(null=True, blank=True, max_length=255)
    endtime=models.CharField(null=True, blank=True, max_length=255)
    isbreak=models.BooleanField(null=True, blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True, blank=True)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True, blank=True)
    batchname=models.ForeignKey(Batch,null=True,blank=True, on_delete=models.CASCADE)
    coursename=models.ForeignKey(Course,null=True,blank=True,on_delete=models.CASCADE)
    academicyearname=models.ForeignKey(Academicyear,null=True,blank=True,on_delete=models.CASCADE)


class AssignTeacher(models.Model):
    academicyearname=models.ForeignKey(Academicyear,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    Name=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    coursename=models.ForeignKey(Course,on_delete=models.CASCADE)
    batchname=models.ForeignKey(Batch,on_delete=models.CASCADE)


class Attendance(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.DateField()
    attendance=models.CharField(max_length=255, null=True, blank=True)
    reason=models.CharField(max_length=255)
    academicyearname = models.ForeignKey(Academicyear, on_delete=models.CASCADE, null=True, blank=True)
    batchname = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.CASCADE)
    coursename = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)





class AttendanceMarked(models.Model):
    date = models.DateField()
    academicyearname=models.ForeignKey(Academicyear,on_delete=models.CASCADE, null=True, blank=True,)
    batchname = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.CASCADE)
    coursename = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,blank=True)

class Category(models.Model):
    category = models.CharField(null=True, blank=True, max_length=255)
    academicyear = models.ForeignKey(Academicyear, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, max_length=255, on_delete=models.CASCADE)
    subcategory = models.CharField(null=True, blank=True, max_length=255)
    amount = models.IntegerField(null=True, blank=True)


class Fee(models.Model):
    coursename = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    batchname = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.CASCADE)
    feecategory = models.CharField(null=True, blank=True, max_length=255)
    subcategory = models.CharField(null=True, blank=True, max_length=255)
    admissionnumber = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    paid = models.IntegerField(null=True, blank=True)
    balance = models.BigIntegerField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    duedate = models.DateField(null=True, blank=True)
    amt = models.IntegerField(null=True, blank=True)
    fine = models.IntegerField(null=True, blank=True)


class Subcategory(models.Model):
    subcategory = models.CharField(null=True, blank=True, max_length=255)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.PROTECT)


class Busdetails(models.Model):
    busnumber=models.IntegerField(null=True,blank=True,)
    buscapacity=models.IntegerField(null=True,blank=True)
    driver=models.CharField(max_length=255, null=True,blank=True,)

class Busstop(models.Model):
    busstop=models.CharField(max_length=255, null=True,blank=True)
    busroute=models.CharField(max_length=255, null=True,blank=True)
    description=models.CharField(max_length=255, null=True,blank=True)
    bno=models.ForeignKey(Busdetails,null=True,blank=True,on_delete=models.PROTECT)


class Busroute(models.Model):
    routename= models.CharField(max_length=255,null=True,blank=True)
    desscription= models.CharField(max_length=255,null=True,blank=True)
    busno=models.ForeignKey(Busdetails,null=True,blank=True,on_delete=models.PROTECT)

class Assign(models.Model):
    busstop = models.ForeignKey(Busstop,null=True, blank=True, on_delete=models.PROTECT)
    transportprice = models.IntegerField(null=True, blank=True)
    route = models.ForeignKey(Busroute,max_length=255, null=True,blank=True,on_delete=models.PROTECT)
    pick = models.CharField(max_length=255, null=True,blank=True)
    Drop = models.CharField(max_length=255, null=True,blank=True)


class Transport(models.Model):
    admissionnumber=models.ForeignKey(Student,null=True, blank=True, on_delete=models.PROTECT)
    coursename=models.ForeignKey(Course,null=True,blank=True, on_delete=models.PROTECT)
    batchname=models.ForeignKey(Batch, null=True, blank=True, on_delete=models.PROTECT)
    route=models.ForeignKey(Assign, null=True, blank=True, on_delete=models.PROTECT)

class Feecategory(models.Model):
    category=models.CharField(max_length=255,null=True,blank=True)

class Feetype(models.Model):
    feetype=models.CharField(max_length=255,null=True,blank=True)


class Feeallocation(models.Model):
    category=models.ForeignKey(Feecategory,null=True,blank=True,on_delete=models.PROTECT)
    type=models.ForeignKey(Feetype,null=True,blank=True,on_delete=models.PROTECT)
    course=models.ForeignKey(Course,null=True,blank=True,on_delete=models.PROTECT)
    amount=models.IntegerField()
    fromdate = models.DateField(auto_now=True)
    Duedate = models.DateField(null=True, blank=True)


class Feecollection(models.Model):
    fee=models.ForeignKey(Feeallocation,null=True,blank=True,on_delete=models.PROTECT)
    admission=models.ForeignKey(Student,null=True,blank=True,on_delete=models.PROTECT)
    course=models.ForeignKey(Course,null=True,blank=True,on_delete=models.PROTECT)
    paid=models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    status=models.CharField(max_length=255)


class PlacementBulk(models.Model):
    admissionyear = models.CharField(max_length=255,null=True,blank=True)
    uploaddata = models.FileField(upload_to="placement/", null=True, blank=True)


class Placement(models.Model):
    admissionno = models.IntegerField(null=True,blank=True)
    admissionyear = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    salary = models.IntegerField()


class HigherStudiesBulk(models.Model):
    admissionyear = models.CharField(max_length=255,null=True,blank=True)
    data = models.FileField(upload_to="higherstudies/", null=True, blank=True)


class HigherStudies(models.Model):
    admissionno = models.IntegerField(null=True,blank=True)
    admissionyear = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    entrancerank = models.IntegerField()
    college = models.CharField(max_length = 255)


class StudentBulk(models.Model):
    admissionyear = models.CharField(max_length=255,null=True,blank=True)
    data = models.FileField(upload_to="studentlist/", null=True, blank=True)
