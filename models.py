from django.db import models

# Create your models here.
class Academicyear(models.Model):
    academicyearname=models.CharField(max_length=255, null=True, blank=True)
    startson=models.DateField(null=True,blank=True)
    endson=models.DateField(null=True,blank=True)
    addondate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    isactive = models.BooleanField(default=False, null=True, blank=True)


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
    addondate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    academicid = models.ForeignKey(Academicyear,null=True, blank=True, on_delete=models.CASCADE)


class Teacher(models.Model):
    Name=models.CharField(max_length=255)
    Designation=models.CharField(max_length=255)
    Education=models.CharField(max_length=255)
    Experiance=models.IntegerField()
    Gender=models.CharField(max_length=255)
    Subject=models.CharField(max_length=255, null=True, blank=True)


class Subject(models.Model):
    subject=models.CharField(max_length=255)
    academicid=models.ForeignKey( Academicyear,on_delete=models.CASCADE,null=True,blank=True,)
    courseid=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True,)

class AssignTeacher(models.Model):
    academicyearname=models.ForeignKey(Academicyear,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    Name=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    coursename=models.ForeignKey(Course,on_delete=models.CASCADE)
    batchname=models.ForeignKey(Batch,on_delete=models.CASCADE)


