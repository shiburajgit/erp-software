
from django.shortcuts import render, redirect,loader
from django.contrib.auth import authenticate, login
from school import models
from school import views
def studentLogin_view(request):
    # admission=models.Student.objects.all()
    if request.method == 'POST':
        username = request.POST.get("adno")
        password = request.POST.get("dob")
        ob = models.Student.objects.filter(AdmissionNumber=username,DOB=password)


        if ob is None:
            print("user not exist")
        else:

            return redirect('studenthome/')
    return render(request, 'studentlogin.html', {})
def student_view(request):
    return render(request, 'studenthomepage.html', {})

def studentviewtimetable(request):
    obj1 = models.Academicyear.objects.get(isactive=True)
    obj2 = models.Course.objects.filter(academicid__isactive=True)
    obj3=''
    obj4=''
    obj5=''
    if request.method=='POST':

        academicyear = request.POST.get('academicyear')
        course = request.POST.get('course')
        batch = request.POST.get('batch')
        obj4=models.Timetable.objects.filter(academicyearname__academicyearname=academicyear,coursename=course,batchname=batch).values('Day').distinct()
        obj3=models.Timetable.objects.filter(academicyearname__academicyearname=academicyear,coursename=course,batchname=batch)
        obj5=models.Timetable.objects.filter(academicyearname__academicyearname=academicyear,coursename=course,batchname=batch,isbreak=False)
    return render(request,'studenttimetableview.html',{'key1':obj1,'key2':obj2,'key3':obj3,'key4':obj4,'key5':obj5})
