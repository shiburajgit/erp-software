from django.shortcuts import render, redirect,loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date
from datetime import datetime as dte
from . import models
from .models import Book, Order, Student, Timetable, Category, Transport, Assign, Busdetails, Busstop, Busroute,Feecategory
from django.contrib import messages
from datetime import datetime, timedelta
import xlrd
import os
from django.core.paginator import Paginator
import PyPDF2
from django.http import HttpResponse
from rest_framework.response import Response




# Create your views here.

def Form(request):
    if request.method == 'POST':
        username = request.POST.get("uname")
        # studclass = request.POST.get("studclass")
        emailid = request.POST.get("email")
        # fine = request.POST.get("fine")
        password = request.POST.get("password")
        confirm_password = request.POST.get("psw")
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=emailid, password=password)
            user.save()
            return redirect('login')
    return render(request, 'form.html', {})


def Login_view(request):
    if request.method == 'POST':
        username = request.POST.get("Username")
        password = request.POST.get("pass")
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is None:
            print("user not exist")
        else:
            login(request, user)
            if user.is_staff:
                return redirect('admin')
            else:
                return redirect('editbook')
    return render(request, 'login.html', {})
#






def Academicyear(request):
    msg=''
    msg1=''
    obj1=models.Academicyear.objects.all()
    if request.method == 'POST' and 'submit' in request.POST:
        academicyearname = request.POST.get("academicyear")
        startson = request.POST.get("startson")
        endson = request.POST.get('endson')
        ob=models.Academicyear.objects.filter(academicyearname=academicyearname)
        print(obj1)
        if not ob:
            obj = models.Academicyear()
            obj.academicyearname = academicyearname
            obj.startson = startson
            obj.endson = endson
            obj.save()
        else:
            msg1 = 'yes'
    if request.method == 'POST' and 'active' in request.POST:
        idd = request.POST.get('active')
        ob = models.Academicyear.objects.exclude(id=idd)
        obj = models.Academicyear.objects.get(id =idd)

        if obj.isactive:
            obj.isactive = False
            msg = "yes"
        else:
            obj.isactive = True
            msg = "no"
            for i in ob:
                i.isactive=False
                i.save()
        obj.save()


    if request.method =='POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.Academicyear.objects.get(id=idd)
        ob.delete()
    return render(request, 'academicyear.html', {'key':obj1,'key1':msg,'key2':msg1})

def editacademicyear(request,id):
    obj = models.Academicyear.objects.get(id=id)
    msg = ''
    if request.method=='POST':
        academicyearname = request.POST.get("academicyear")
        startson = request.POST.get("startson")
        endson = request.POST.get('endson')
        ob=models.Academicyear.objects.filter(academicyearname=academicyearname)
        if not ob:
            obj.academicyearname = academicyearname
            obj.startson = startson
            obj.endson = endson
            obj.save()
            return redirect('academicyear')
        else:
            msg='yes'
    return render(request,'editacademicyear.html',{'key':obj,'key1':msg})


def Course_view(request):
    obj1 = models.Academicyear.objects.get(isactive = True)
    obj2 = models.Course.objects.all()
    msg=''
    if request.method == 'POST' and 'submit' in request.POST:
        course = request.POST.get("course")
        academicyear = request.POST.get('academicyear')
        ob=models.Course.objects.filter(coursename=course)
        if not ob:
            obj = models.Course()
            obj.coursename = course
            obj.academicid  = models.Academicyear.objects.get(academicyearname=academicyear)
            obj.save()
        else:
            msg = 'yes'

    if request.method =='POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.Course.objects.get(id=idd)
        ob.delete()
    return render(request, 'course.html', {"key": obj1,"key2":obj2,'key3':msg})

def editcourse(request,id):
    obj = models.Course.objects.get(id=id)
    msg=''

    if request.method == 'POST':
        course = request.POST.get("course")
        academicyear = request.POST.get('academicyear')
        ob= models.Course.objects.filter(coursename=course,academicid__academicyearname=academicyear)
        if not ob:
            obj.coursename = course
            obj.academicid =models.Academicyear.objects.get(academicyearname=academicyear)
            obj.save()
            return redirect('course')
        else:
             msg='yes'

    return render(request, 'editcourse.html', {'key':obj,'key1':msg})


def Batch(request):
    ob = models.Academicyear.objects.get(isactive=True)
    obj1 = models.Batch.objects.all()
    obj2 = models.Course.objects.filter(academicid__isactive=True)
    msg=''
    if request.method == 'POST' and 'submit' in request.POST:
        batch = request.POST.get("batch")
        course = request.POST.get("course")
        academicyear = request.POST.get('academicyear')
        ob1=models.Batch.objects.filter(batchname=batch,courseid=course,academicid__academicyearname=academicyear)
        if not ob1:
            obj = models.Batch()
            obj.batchname = batch
            obj.academicid = models.Academicyear.objects.get(academicyearname=academicyear)
            obj.courseid = models.Course.objects.get(id=course)
            obj.save()
        else:
            msg='yes'

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.Batch.objects.get(id=idd)
        ob.delete()

    return render(request, 'batch.html', {'key1': obj1, 'key2': obj2, 'key':ob,'key3':msg})


def editbatch(request,id):
    obj=models.Batch.objects.get(id=id)
    obj1=models.Course.objects.filter(academicid__isactive=True)
    msg =''
    if request.method == 'POST':
        batch=request.POST.get("batch")
        course = request.POST.get("course")
        academicyear = request.POST.get('academicyear')
        ob=models.Batch.objects.filter(batchname=batch,courseid__coursename=course,academicid__academicyearname=academicyear)
        if not ob:
            obj.batchname = batch
            obj.academicid =models.Academicyear.objects.get(academicyearname=academicyear)
            obj.courseid=models.Course.objects.get(coursename=course)
            obj.save()
            return redirect('batch')
        else:
            msg='yes'
    return render(request,'editbatch.html',{'key':obj,'key1':obj1,'key2':msg})


def quata(request):
    obj=models.Quata.objects.all()
    if request.method=='POST' and 'submit' in request.POST:
        quata=models.Quata()
        quata.AdmittedQuata=request.POST.get('quata')
        quata.save()
    if request.method=='POST' and 'delete' in request.POST:
        idd=request.POST.get('delete')
        ob=models.Quata.objects.get(id=idd)
        ob.delete()
    return render(request,'quata.html',{'obj':obj})

def editquata(request,id):
    ob=models.Quata.objects.get(id=id)
    if request.method=='POST':
        ob.AdmittedQuata=request.POST.get('quata')
        ob.save()
        return redirect('quata')
    return render(request,'editquata.html',{'ob':ob})


def Subject(request):
    ob = models.Academicyear.objects.get(isactive=True)
    obj1 = models.Course.objects.filter(academicid__isactive=True)
    obj2 = models.Subject.objects.all()
    msg=''
    filepath ='media/syllabus/'
    if request.method == 'POST' and 'submit' in request.POST:
        subject=request.POST.get('subject')
        course = request.POST.get("course")
        academicyear = request.POST.get('academicyear')
        file = request.FILES['file']


        ob1=models.Subject.objects.filter(subject=subject,courseid=course,academicid__academicyearname=academicyear)
        if not ob1:
            obj = models.Subject()
            obj.subject=subject
            obj.academicid = models.Academicyear.objects.get(academicyearname=academicyear)
            obj.courseid = models.Course.objects.get(id=course)
            obj.syllabus = file
            obj.save()



        else:
            msg='yes'

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.Subject.objects.get(id=idd)
        ob.delete()
    return render(request, 'subject.html', {'key': ob,'key1':obj1,'key2':obj2,'key3':msg})

def syllabus(request,id):
    # filepath='media/'
    msg='Syllabus not Uploaded'
    file=models.Subject.objects.get(id=id)

    return render(request,'syllabus.html',{'file':file,'msg':msg})

def editsubject(request,id):
    obj=models.Subject.objects.get(id=id)
    obj1 = models.Course.objects.filter(academicid__isactive=True)
    msg=''
    if request.method == 'POST':
        subject=request.POST.get("subject")
        course = request.POST.get("course")
        academicyear = request.POST.get('academicyear')
        file = request.FILES['file']
        ob=models.Subject.objects.filter(academicid__academicyearname=academicyear,courseid__coursename=course,subject=subject, syllabus=file)
        if not ob:
            obj.subject = subject
            obj.academicid =models.Academicyear.objects.get(academicyearname=academicyear)
            obj.courseid=models.Course.objects.get(coursename=course)
            obj.syllabus = file
            obj.save()
            return redirect('subject')
        else:
            msg='yes'
    return render(request,'editsubject.html',{'key':obj, 'key1':obj1,'key2':msg})


def Admin_view(request):
    return render(request, 'admin.html', {})


def Admission(request):
    obj1 = models.Academicyear.objects.get(isactive=True)
    obj2 = models.Course.objects.filter(academicid__isactive=True)
    obj3 = models.Quata.objects.all()
    msg=''
    if request.method == "POST" and 'submit' in request.POST:

        admissionnumber = request.POST.get("admissionnumber")
        admissionyear = request.POST.get("admissionyear")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        emailid = request.POST.get("email")
        dateofbirth = request.POST.get("dob")
        bloodgroup = request.POST.get("bloodgroup")
        phonenumber = request.POST.get("phonenumber")
        contactdetails = request.POST.get("contactdetails")
        gender = request.POST.get("gender")
        rollno = request.POST.get("rollno")
        batch = request.POST.get("batch")
        quata = request.POST.get("quata")
        academicyear = request.POST.get("academicyear")
        course = request.POST.get("course")
        obj3 = models.Batch.objects.filter(id=course)
        ob =models.Student.objects.filter(AdmissionNumber=admissionnumber)
        if not ob:
            obj = models.Student()
            obj.AdmissionNumber = admissionnumber
            obj.AdmissionYear = admissionyear
            obj.FirstName = firstname
            obj.LastName = lastname
            obj.Email = emailid
            obj.DOB = dateofbirth
            obj.BloodGroup = bloodgroup
            obj.PhoneNumber = phonenumber
            obj.ContactDetails = contactdetails
            obj.Gender = gender
            obj.academicyear = models.Academicyear.objects.get(academicyearname=academicyear)
            obj.RollNo = rollno
            obj.course = models.Course.objects.get(id=course)
            # obj.Batch = models.Batch.objects.get(id=batch)
            obj.RollNo=rollno
            obj.Batch = models.Batch.objects.get(id=batch)
            obj.AdmittedQuata = models.Quata.objects.get(id=quata)
            obj.save()
            return redirect('studentlist')
        else:
            msg = 'yes'
    return render(request, 'admission.html', {'key1': obj1, 'key2': obj2,'key3':msg,'key4':obj3})


def teacherdetails(request):
    msg=''
    if request.method == "POST":
        Name = request.POST.get("name")
        Designation = request.POST.get("designation")
        Education = request.POST.get("education")
        Experiance = request.POST.get("experiance")
        Gender = request.POST.get("gender")
        ob=models.Teacher.objects.filter(Name=Name,Designation=Designation,Education=Education,Experiance=Experiance,Gender=Gender)
        print(ob)
        if not ob:
            obj = models.Teacher()
            obj.Name = Name
            obj.Designation = Designation
            obj.Education = Education
            obj.Experiance = Experiance
            obj.Gender = Gender
            obj.save()
            return redirect('teacherlist')
        else:
            msg = 'yes'
    return render(request, 'teacherdetails.html', {'key':msg})


def teacherlist(request):
    obj = models.Teacher.objects.all()
    if request.method == 'POST' and 'delete' in request.POST:
        idd =request.POST.get('delete')
        ob = models.Teacher.objects.get(id=idd)
        ob.delete()
    return render(request, 'teacherlist.html', {'key': obj})
def assignteacher(request):
    obj1 = models.Academicyear.objects.get(isactive = True)
    obj2= models.Course.objects.filter(academicid__isactive= True)
    obj5=models.Teacher.objects.all()
    obj6=models.AssignTeacher.objects.all()
    msg=''
    if request.method=='POST' and 'assignteacher' in request.POST:
        academicyearname=request.POST.get("academicyear")
        coursename=request.POST.get("coursename")
        batchname=request.POST.get('batchname')
        subject=request.POST.get("subject")
        teacher=request.POST.get("teacher")
        ob=models.AssignTeacher.objects.filter(academicyearname__academicyearname=academicyearname,coursename=coursename,batchname=batchname,subject=subject,Name=teacher)
        if not ob:
            obj=models.AssignTeacher()
            obj.academicyearname=models.Academicyear.objects.get(academicyearname=academicyearname)
            obj.coursename=models.Course.objects.get(id=coursename)
            obj.batchname=models.Batch.objects.get(id=batchname)
            obj.subject=models.Subject.objects.get(id=subject)
            obj.Name=models.Teacher.objects.get(id=teacher)
            obj.save()
        else:
            msg='yes'
    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.AssignTeacher.objects.get(id=idd)
        ob.delete()
    return render(request,'assignteacher.html',{'key':obj6, 'key1':obj1,'key2':obj2,'key5':obj5,'key3':msg})


def editassignteacher(request,id):
    obj=models.AssignTeacher.objects.get(id=id)
    obj1=models.Academicyear.objects.get(isactive=True)
    obj2=models.Course.objects.filter(academicid__isactive =True)
    obj3=models.Teacher.objects.all()
    if request.method == 'POST':
        academicyear=request.POST.get('academicyear')
        obj.academicyearname=models.Academicyear.objects.get(academicyearname=academicyear)
        course=request.POST.get("coursename")
        obj.coursename=models.Course.objects.get(id=course)
        batch=request.POST.get("batchname")
        obj.batchname=models.Batch.objects.get(id=batch)
        subject=request.POST.get("subject")
        obj.subject=models.Subject.objects.get(id=subject)
        teacher=request.POST.get("teacher")
        obj.Name=models.Teacher.objects.get(id=teacher)
        obj.save()
        return redirect('assignteacher')
    return render(request,'editassignteacher.html',{'key':obj,'key1':obj1,'key2':obj2,'key3':obj3})


def editteacher(request, id):
    obj =models.Teacher.objects.get(id=id)
    if request.method =="POST":
        Name = request.POST.get("name")
        Designation = request.POST.get("designation")
        Education = request.POST.get("education")
        Experiance = request.POST.get("experiance")
        Subject =request.POST.get("subject")
        Gender = request.POST.get("gender")

        obj.Name=Name
        obj.Designation=Designation
        obj.Education=Education
        obj.Experiance=Experiance
        obj.Subject=Subject
        obj.Gender=Gender
        obj.save()
        return redirect('teacherlist')

    return render(request,'editteacher.html',{'key':obj})



def Studentlist(request):
    scourseid=''
    sacademicid=''
    squataid=''
    stbatchid=''
    date=''
    objlist = Student.objects.all()
    paginator = Paginator(objlist, 50)
    page = request.GET.get('page')
    obj = paginator.get_page(page)


    if request.method == 'POST' and 'search' in request.POST:
        admissionyear = request.POST.get('admissionyear')
        file = request.FILES['file']

        filepath = 'media/studentlist/'
        data = os.path.join(str(filepath),str(file))

        if os.path.isfile(data):
            os.remove(data)
        else:
            pass

        higher = models.StudentBulk()
        higher.admissionyear = admissionyear
        higher.data = file
        higher.save()
        path = os.path.join(str(filepath), str(file))

        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        row = sheet.nrows

        for i in range(1,row):
            adm=sheet.cell_value(i,1)
            name=sheet.cell_value(i,2)
            # dob=sheet.cell_value(i,3)
            branch=sheet.cell_value(i,10)
            gender=sheet.cell_value(i,15)
            quata=sheet.cell_value(i,5)
            academicyear=sheet.cell_value(i,32)
            batch=sheet.cell_value(i,33)
            if sheet.cell(i, 3).ctype == 3:
                    ms_date_number = sheet.cell(i, 1).value  # Correct option 2
                    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number, wb.datemode)
                    py_date = dte(year, month, day)
                    date = py_date.date()
            Academicyear = models.Academicyear.objects.filter(academicyearname=academicyear)
            if not Academicyear:
                sacademic = models.Academicyear()
                sacademic.academicyearname = academicyear
                sacademic.save()
                sacademic = models.Academicyear.objects.filter(academicyearname=academicyear)
                for l in sacademic:
                    sacademicid = l.id
            else:
                sacademic = models.Academicyear.objects.filter(academicyearname=academicyear)
                for l in sacademic:
                    sacademicid = l.id

            Course = models.Course.objects.filter(coursename=branch,academicid=sacademicid)
            if not Course:
                scourse = models.Course()
                scourse.coursename = branch
                scourse.academicid = models.Academicyear.objects.get(id=sacademicid)
                scourse.save()
                scourse = models.Course.objects.filter(coursename=branch,academicid=sacademicid)
                for k in scourse:
                    scourseid = k.id
                    print('lllll',scourse)
            else:
                scourse = models.Course.objects.filter(coursename=branch,academicid=sacademicid)
                for k in scourse:
                    scourseid = k.id
            print(batch,'llllll',sacademicid,scourseid)
            batchc = models.Batch.objects.filter(batchname=batch, academicid=sacademicid, courseid=scourseid).exists()
            if not batchc:
                print('aaaaaa')
                stbatch = models.Batch()
                print (sacademicid,scourseid,batch)
                stbatch.batchname=batch
                stbatch.academicid=models.Academicyear.objects.get(id=sacademicid)
                stbatch.courseid = models.Course.objects.get(id=scourseid)
                stbatch.save()
                stbatch = models.Batch.objects.filter(batchname=batch, academicid=sacademicid, courseid=scourseid)
                for n in stbatch:
                    print('bbbbb')
                    stbatchid = n.id
            else:
                stbatch = models.Batch.objects.filter(batchname=batch, academicid=sacademicid, courseid=scourseid)
                for n in stbatch:
                    stbatchid = n.id
            Quata = models.Quata.objects.filter(AdmittedQuata=quata)
            if not Quata:
                squata = models.Quata()
                squata.AdmittedQuata = quata
                squata.save()
                squata = models.Quata.objects.filter(AdmittedQuata=quata)
                for m in squata:
                    squataid = m.id
            else:
                squata = models.Quata.objects.filter(AdmittedQuata=quata)
                for m in squata:
                    squataid = m.id

            obj1 = models.Student.objects.filter(AdmissionNumber=int(adm),AdmissionYear=academicyear,FirstName=name,DOB=date,Gender=gender,academicyear=sacademicid,
                                                 course=scourseid,Batch=stbatchid,AdmittedQuata=squataid)

            if not obj1:
                models.Student.objects.create(AdmissionNumber=int(adm),Batch_id=stbatchid,FirstName=name,DOB=date,
                                              Gender=gender,academicyear_id=sacademicid,course_id=scourseid,
                                              AdmittedQuata_id=squataid,AdmissionYear=academicyear)
            else:
                pass

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = Student.objects.get(id=idd)
        ob.delete()
    return render(request, 'new.html', {'key': obj})


def Editstudent(request, id):
    obj = Student.objects.get(id=id)
    obj1 = models.Academicyear.objects.get(isactive=True)
    obj2 = models.Course.objects.filter(academicid__isactive=True)
    obj3 = models.Quata.objects.all()

    if request.method == 'POST':
        admissionnumber = request.POST.get("admissionnumber")
        obj.AdmissionNumber = admissionnumber
        admissionyear = request.POST.get("admissionyear")
        obj.AdmissionYear = admissionyear
        firstname = request.POST.get("firstname")
        obj.FirstName = firstname
        lastname = request.POST.get("lastname")
        obj.LastName = lastname
        emailid = request.POST.get("email")
        obj.Email = emailid
        dateofbirth = request.POST.get("dob")
        obj.DOB = dateofbirth
        bloodgroup = request.POST.get("bloodgroup")
        obj.BloodGroup = bloodgroup
        phonenumber = request.POST.get("phonenumber")
        obj.PhoneNumber = phonenumber
        contactdetails = request.POST.get("contactdetails")
        obj.ContactDetails = contactdetails
        gender = request.POST.get("gender")
        obj.Gender = gender
        rollno = request.POST.get("rollno")
        obj.RollNo = rollno
        batch = request.POST.get("batch")
        obj.batch = batch
        quata = request.POST.get("quata")
        obj.AdmittedQuata=quata
        obj.save()
        return redirect('studentlist')
    return render(request, 'editstudent.html', {"key":obj,'key1':obj1, 'key2':obj2,'key3':obj3})


def order(request):
    today = date.today()
    u=''
    v=''
    msg = ''
    fine=0
    stud=''
    AdmissionNumber=''
    obj = models.Student.objects.all()
    if request.method == 'POST':


        if 'issue' in request.POST:
            AdmissionNumber = int(request.POST.get("admissionnumber"))
            BookName = request.POST.get("bookname")
            student = Student.objects.get(id=AdmissionNumber)
            print(AdmissionNumber,student)
            u = Student.objects.filter(id=AdmissionNumber)
            print(u,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            v = Order.objects.filter(student=student)

            try:
                if BookName == '':
                    pass
                else:
                    BookName = Book.objects.get(BookName=BookName)
                    t = Order.objects.filter(student=student, returndate=None)
                    s = Order.objects.filter(returndate=None, BookName=BookName, student=student)
                    if BookName.Number > 0:
                        if len(t) < 2 and len(s) == 0:
                            obj1 = Order()
                            print('--------------------------')
                            obj1.student = student
                            obj1.BookName = BookName
                            obj1.duedate = datetime.now() + timedelta(days=15)
                            obj1.save()
                            BookName.Number -= 1
                            BookName.save()
                    else:
                        msg = "yes"
            except:
                msg = "No"

        if 'return' in request.POST:

                admissionnumber = request.POST.get("admissionnumber")
                BookName = request.POST.get("bookname")
                student = Student.objects.get(id=admissionnumber)
                u = Student.objects.filter(AdmissionNumber=admissionnumber)
                v = Order.objects.filter(student=student)

                if BookName == '':
                    pass
                else:

                    student = Student.objects.get(id=admissionnumber)
                    print(student,'kllll')
                    BookName = Book.objects.get(BookName=BookName)
                    obj = Order.objects.filter(student=student, BookName=BookName, returndate=None)
                    # stud = Order.objects.filter(student=student,BookName=BookName)

                    if len(obj)>0:
                        for i in obj:
                            i.returndate = today
                            i.save()
                        BookName.Number += 1
                        BookName.save()
                    else:
                        print("Something went wrong")

                    for i in obj:
                        delay = i.returndate - i.issuedate
                        if delay.days > 15:
                            for d in range(16,delay.days+1):
                                fine = fine + 1
                        else:
                            fine = 0
                        i.fine = fine
                        i.save()



    return render(request, 'vieworder.html',{'key1' : msg,'key2' : u, 'key' : v, 'key3':obj, 'key4': AdmissionNumber})

def Orderlist(request):
    ob= models.Order.objects.all()
    obj=''
    if request.method == 'POST':
        fromdate = request.POST.get("fromdate")
        todate = request.POST.get("todate")
        # obj = models.Order.objects.filter(issuedate=issuedate)
        obj=models.Order.objects.filter(issuedate__range=[fromdate, todate])
        print(obj)
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    return render(request,'orderlist.html',{'key': ob,'key1':obj})



def Period(request):
    # academicyearname = models.Academicyear.objects.all()
    # coursename = models.Course.objects.all()
    # batchname = models.Batch.objects.all()
    obj=models.Subject.objects.all()
    obj1=models.Timetable.objects.all()
    # obj2=models.Timetable.objects.get(id=id)
    if request.method =='POST' and 'submit' in request.POST:
        print("bbbbbbbbbbbbbbbbbbbbbbbbb")
        day=request.POST.get('day')
        period1= request.POST.get('period1')
        period2 = request.POST.get('period2')
        period3 = request.POST.get('period3')
        period4 = request.POST.get('period4')
        period5 = request.POST.get('period5')
        period6 = request.POST.get('period6')
        academicyearname=request.POST.get('academicyearname')
        coursename=request.POST.get('coursename')
        batchname=request.POST.get('batchname')
    #
        obj1=models.Timetable()
        obj1.Day=day
        obj1.period1=period1
        obj1.period2 = period2
        obj1.period3 = period3
        obj1.period4 = period4
        obj1.period5 = period5
        obj1.period6 = period6
        obj1.academicyearname=models.Academicyear.objects.get(id=academicyearname)
        obj1.coursename=models.Course.objects.get(id=coursename)
        obj1.batchname=models.Batch.objects.get(id=batchname)
        print('###############################################')
        print(obj1)
        obj1.save()
        return redirect('timetable')

    #
    academicyearname=request.POST.get("academicyearname")
    coursename=request.POST.get("coursename")
    batchname=request.POST.get("batchname")
    return render(request,'period.html',{'key':obj,'key1':obj1,'key2':academicyearname,'key3':coursename,'key4':batchname})


def EditPeriod(request,id):
    ob = models.Subject.objects.all()
    obj1 = models.Timetable.objects.get(id=id)
    if request.method == 'POST':
        day = request.POST.get('day')
        period1 = request.POST.get('period1')
        period2 = request.POST.get('period2')
        period3 = request.POST.get('period3')
        period4 = request.POST.get('period4')
        period5 = request.POST.get('period5')
        period6 = request.POST.get('period6')
        obj1.Day = day
        obj1.period1 = period1
        obj1.period2 = period2
        obj1.period3 = period3
        obj1.period4 = period4
        obj1.period5 = period5
        obj1.period6 = period6
        obj1.save()
        return redirect('timetable')
    return render(request,'editperiod.html',{'key':ob})

def timetableset(request):
    return render(request,'set period.html',{})


def periodselection(request):
    return render(request,'periodselection.html',{})

def attendance(request):
    o=''
    o1=''
    o2=''
    o3=''
    obj1 = models.Academicyear.objects.get(isactive=True)
    obj2=models.Course.objects.filter(academicid__isactive=True)
    msg=''
    obj4=''
    obj5=''



    academicyear = request.POST.get('academicyear')
    course = request.POST.get('coursename')
    batch = request.POST.get('batchname')
    date = request.POST.get('date')
    subject=request.POST.get('subject')
    print(subject)
    print('+++++++',date)
    mark = models.AttendanceMarked.objects.filter(date=date, academicyearname__academicyearname=academicyear,coursename_id=course,batchname_id=batch,subject_id=subject)
    print('aaaaaaa',mark)
    if not mark:
         obj4 = models.Student.objects.filter(academicyear__academicyearname=academicyear, course_id=course,
                                          Batch_id=batch)
    else:
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        obj4 = models.Student.objects.filter(academicyear__academicyearname=academicyear, course_id=course,Batch_id=batch).values()

        obj5 = models.Attendance.objects.filter(academicyearname__academicyearname=academicyear, coursename_id=course,subject_id=subject,
                                                batchname_id=batch,date=date).values()

        # for j in obj5:
        #     print('oooo',j.date)
        print('-----',obj5)
        # print(obj4)
        for j in obj5:
            # print(j.date)
            for i in obj4:

                if i['id'] == j['student_id']:
                    # print(i['AdmissionNumber'],j.student.AdmissionNumber)
                    print("aaaaaaaa")
                    i['attendance'] = 'absent'
                    i['reason'] = j['reason']
                    print (i['attendance'])


        for i in obj4:
            if 'attendance' in obj4:
                print ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa',i['attendance'])


    if request.method =='POST' and 'search' in request.POST:

        academicyear = request.POST.get('academicyear')
        course = request.POST.get('coursename')
        batch = request.POST.get('batchname')
        date = request.POST.get('date')
        subject=request.POST.get('subject')
        mark = models.AttendanceMarked.objects.filter(date=date, academicyearname__academicyearname=academicyear,coursename_id=course,batchname_id=batch, subject=subject)

        if not mark:

            ob = models.AttendanceMarked()
            ob.date = date
            ob.academicyearname=models.Academicyear.objects.get(academicyearname=academicyear)
            ob.coursename=models.Course.objects.get(id=course)
            ob.batchname=models.Batch.objects.get(id=batch)
            ob.subject=models.Subject.objects.get(id=subject)
            ob.save()
        else:
            msg='yes'

        o=models.Academicyear.objects.get(academicyearname=academicyear)
        o1=models.Course.objects.get(id=course)
        o2=models.Batch.objects.get(id=batch)
        o3=models.Subject.objects.get(id=subject)


    if request.method == 'POST' and 'submit' in request.POST:

         #reason = request.POST.get('reason')
        #student = request.POST.get('student')
        academicyear = request.POST.get('academicyearid')
        course = request.POST.get('courseid')
        batch = request.POST.get('batchid')
        date = request.POST.get('date')
        subject = request.POST.get('subjectid')
        print(academicyear, course, batch, date)
        if not mark:
             obj4 = models.Student.objects.filter(academicyear__id=academicyear, course_id=course,
                                                  Batch_id=batch)
        else:
             pass
        print(obj4, len(obj4))
        for i in range(len(obj4)):
             obj = models.Attendance()
             obj.academicyearname = models.Academicyear.objects.get(id=academicyear)
             obj.coursename = models.Course.objects.get(id=course)
             obj.batchname = models.Batch.objects.get(id=batch)
             obj.subject=models.Subject.objects.get(id=subject)
             obj.student = models.Student.objects.get(id=request.POST.get('student'+str(i)))
             obj.date = date
             obj.attendance = request.POST.get('attendance' + str(i))
             obj.reason = request.POST.get('reason' + str(i))
             if obj.attendance == '1':
                 print('saved')
                 obj.save()
             else:
                 pass
        obj4=''
    return render(request,'attendance.html',{'key1':obj1,'key2':obj2,'key4':obj4,'key5':date,'o':o,'o1':o1,'o2':o2,'o3':o3,'msg':msg,'obj5':obj5})

def attendance_view(request):
    obj=models.Attendance.objects.all()
    return render(request, 'attendanceview.html',{'key':obj})
def history(request):
    obj = Order.objects.exclude(returndate=None)
    return render(request, 'history.html', {'key': obj})


def edit(request, id):
    obj = User.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get("username")
        obj.username = username
        # studclass = request.POST.get("studclass")
        # obj.studclass = studclass
        email = request.POST.get("email")
        obj.email = email
        # fine = request.POST.get("fine")
        # obj.fine = fine
        obj.save()
        return redirect('student')
    return render(request, 'edit.html', {'key': obj})


def search(request):
    obj = Book.objects.filter(BookName=request.POST.get("bname"), Number__gt=0)
    return render(request, 'search.html', {'key': obj})


def editbook(request, id):
    obj = Book.objects.get(id=id)
    if request.method == 'POST':
        BookName = request.POST.get("bookname")
        obj.BookName = BookName
        AuthorName = request.POST.get("authorname")
        obj.AuthorName = AuthorName
        category = request.POST.get("category")
        obj.category=category
        Count=request.POST.get("total")
        obj.TotalCount=Count
        Number = request.POST.get("number")
        obj.Number = Number
        obj.save()
        return redirect('book')
    return render(request, 'editbook.html', {'key':obj})


def bookform(request):
    if request.method == 'POST':
        BookName = request.POST.get("bookname")
        AuthorName = request.POST.get("authorname")
        category=request.POST.get("category")
        Number = request.POST.get("number")
        Count=request.POST.get("total")
        print(BookName, AuthorName, Number)
        book = Book.objects.create(BookName=BookName, AuthorName=AuthorName,category=category, Number=Number,TotalCount=Count)
        book.save()
        return redirect("book")
    return render(request, 'bookform.html', {})


def book(request):
    obj = Book.objects.all()
    if request.method =='POST' and 'search' in request.POST:
        obj = Book.objects.filter(BookName=request.POST.get("bookname"), Number__gt=0)
    else:
        pass
    if request.method == 'POST' and 'add' in request.POST:
        return redirect('bookform')
    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = Book.objects.get(id=idd)
        ob.delete()
    return render(request, 'book.html', {'key': obj})


def Studentadmin(request):
    return render(request, 'studentadmin.html', {})


def addfee(request):
    error_message = ""
    fine = 0
    ob = ''
    obj1 = models.Student.objects.all()
    obj2 = models.Course.objects.all()
    obj3 = models.Batch.objects.all()
    obj4 = models.Category.objects.all()
    obj5 = models.Subcategory.objects.all()
    balance = None

    if request.method == "POST":
        admissionnumber = request.POST.get("admissionnumber")
        coursename = request.POST.get("course")
        batchname = request.POST.get("batch")
        feecategory = request.POST.get("category")
        subcategory = request.POST.get("subcategory")
        date = request.POST.get("date")
        duedate = request.POST.get("duedate")
        amt = request.POST.get("paid")
        paid = request.POST.get("paid")
        # print(paid+"test")
        # cat=models.Category.objects.get(category=feecategory)

        try:
            ob2 = models.Fee.objects.filter(admissionnumber=admissionnumber).last()
            balance = ob2.balance
        except:
            balance = 0

        obj = models.Fee()
        obj.admissionnumber = models.Student.objects.get(id=admissionnumber)
        obj.coursename = models.Course.objects.get(id=coursename)
        obj.batchname = models.Batch.objects.get(id=batchname)
        obj.feecategory = feecategory
        obj.subcategory = subcategory
        obj.amt = amt
        obj.paid = paid
        a = models.Category.objects.get(category=feecategory)

        if balance == 0:
            obj.balance = int(a.amount) - int(paid)
        if balance != 0:
            obj.balance = balance - int(paid)
            obj.save()

        obj.duedate = datetime.now() + timedelta(days=15)
        obj.save()
        delay = obj.duedate.day - obj.date.day
        if delay > 15:
            fine = fine + 10
        else:
            fine = 0
        obj.fine = fine
        obj.save()
        ob = models.Fee.objects.filter(admissionnumber=admissionnumber)

    return render(request, 'addfee.html',
                  {'key1': obj1, 'key2': obj2, 'key3': obj3, 'key4': obj4, 'key5': ob, 'key6': obj5})


def category(request):
    obj1 = models.Academicyear.objects.all()
    obj2 = models.Course.objects.all()
    obj3 = models.Category.objects.all()
    if request.method == "POST":
        academicyear = request.POST.get("academicyearname")
        course = request.POST.get("coursename")
        category = request.POST.get("category")
        subcategory = request.POST.get("subcategory")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        obj = Category()
        obj.academicyear = models.Academicyear.objects.get(id=academicyear)
        obj.course = models.Course.objects.get(id=course)
        obj.category = category
        obj.amount = amount
        obj.date = date
        obj.save()

    return render(request, 'category.html', {'key1': obj1, 'key2': obj2, 'key3': obj3})


def subcategory(request):
    obj1 = models.Course.objects.all()
    obj2 = models.Subcategory.objects.all()
    if request.method == "POST":
        course = request.POST.get("coursename")
        subcategory = request.POST.get("subcategory")

        obj = models.Subcategory()
        obj.course = models.Course.objects.get(id=course)
        obj.subcategory = subcategory
        obj.save()

    return render(request, 'subcategory.html', {'key1': obj1, 'key2': obj2})


def report(request):
    obj1 = models.Transport.objects.all()
    obj2 = models.Batch.objects.all()

    if request.method == "POST":
        course = request.POST.get("coursename")
        batch = request.POST.get("batchname")

        obj = category()
        obj.course = models.Course.objects.all()
        obj.batch = models.Batch.objects.all()
        obj.save()

    return render(request, 'report.html', {'key1': obj1, 'key2': obj2})




def addtransport(request):
    obj1 = models.Transport.objects.all()
    print(obj1)
    if request.method == 'POST':
        name = request.POST.get("routename")
        price = request.POST.get("transportprice")
        print(name, price)
        obj = Transport()
        obj.routename = name
        obj.transportprice = price
        obj.save()
        return redirect('transport')

    return render(request, 'addtransport.html', {'key1': obj1})


def edittransport(request, id):
    obj = Transport.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get("routename")
        price = request.POST.get("transportprice")

        obj.routename = name
        obj.transportprice = price
        obj.save()

        return redirect('transport')

    return render(request, 'edittransport.html', {'key': obj})


def transport(request):
    msg=''
    obj7= ''
    obj1 = models.Student.objects.all()
    obj2 = models.Course.objects.all()
    obj3 = models.Batch.objects.all()
    obj4 = models.Busroute.objects.all()
    obj5 = models.Transport.objects.all()
    obj6 = models.Assign.objects.all()
    if request.method == "POST":
        admissionnumber = request.POST.get("admissionnumber")
        course = request.POST.get("coursename")
        route = request.POST.get("routename")
        amount = request.POST.get("amount")
        ob=models.Transport.objects.filter(admissionnumber=admissionnumber)
        if not ob:
            print('+++++++dddddd')
            obj = Transport()
            obj.admissionnumber = models.Student.objects.get(id=admissionnumber)
            obj.coursename = models.Course.objects.get(id=course)
            obj.route = models.Assign.objects.get(id=route)
            obj.save()
        else:
            msg='yes'

    return render(request, 'transport.html',
                  {'key1': obj1, 'key2': obj2, 'key3': obj3, 'key4': obj4, 'key5': obj5, 'key6': obj6,'msg':msg})


def busdetails(request):
    obj1 = models.Busdetails.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = Busdetails.objects.get(id=idd)
        obj.delete()
    return render(request, 'busdetails.html', {'key1': obj1})

def busadd(request):
    obj1=Busdetails.objects.all()
    if request.method=='POST':


            busnumber = request.POST.get("busnumber")
            buscapacity = request.POST.get("buscapacity")
            driver = request.POST.get("driver")

            obj = Busdetails()
            obj.busnumber = busnumber
            obj.buscapacity = buscapacity
            obj.driver = driver
            obj.save()
            return redirect('busdetails')
    return render(request, 'busadd.html', {'key1': obj1})

def busedit(request,id):
    ob=Busdetails.objects.get(id=id)
    ob1=Busdetails.objects.all()
    if request.method=='POST':
            busnumber = request.POST.get("busnumber")
            buscapacity = request.POST.get("buscapacity")
            driver = request.POST.get("driver")


            ob.busnumber = busnumber
            ob.buscapacity = buscapacity
            ob.driver = driver
            ob.save()
            return redirect('busdetails')
    return render(request, 'busedit.html', {'key1': ob})

def busstop(request):
    obj1 = models.Busdetails.objects.all()
    obj2 = models.Busstop.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = Busstop.objects.get(id=idd)
        obj.delete()

    return render(request, 'busstop.html', {'key1': obj1, 'key2': obj2})



def stopadd(request):
    obj1 = models.Busdetails.objects.all()
    obj2 = models.Busstop.objects.all()
    if request.method == 'POST':
        busstop = request.POST.get("busstop")
        busroute = request.POST.get("busroute")
        description = request.POST.get("description")
        bno = request.POST.get("busnumber")

        obj = Busstop()
        obj.busstop = busstop
        obj.busroute = busroute
        obj.bno = models.Busdetails.objects.get(id=bno)
        obj.description = description
        obj.save()
        return redirect('busstop')
    return render(request, 'stopadd.html', {'key1': obj1, 'key2': obj2})

def stopedit(request,id):
    ob= models.Busstop.objects.get(id=id)
    obj1 = models.Busdetails.objects.all()
    obj2= models.Busstop.objects.all()
    if request.method == 'POST':
        busstop = request.POST.get("busstop")
        busroute = request.POST.get("busroute")
        description = request.POST.get("description")
        bno = request.POST.get("busnumber")

        ob.busstop = busstop
        ob.busroute = busroute
        ob.bno = models.Busdetails.objects.get(id=bno)
        ob.description = description
        ob.save()
        return redirect('busstop')
    return render(request, 'stopedit.html', {'key1': obj1, 'key2': obj2,'key3':ob})

def assign(request):
    obj1 = models.Busstop.objects.all()
    obj2 = models.Busroute.objects.all()
    obj3 = models.Assign.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = Assign.objects.get(id=idd)
        obj.delete()
    return render(request, 'assign.html', {"key1": obj1, 'key2': obj2, 'key3': obj3})

def assignadd(request):
    obj1 = models.Busstop.objects.all()
    obj2 = models.Busroute.objects.all()
    obj3 = models.Assign.objects.all()

    if request.method == "POST":
        busstop = request.POST.get("busstop")
        busroute = request.POST.get("busroute")
        drop = request.POST.get("droptime")
        pick = request.POST.get("picktime")
        amount = request.POST.get("transportprice")

        obj = models.Assign()
        obj.busstop = models.Busstop.objects.get(id=busstop)
        obj.route = models.Busroute.objects.get(id=busroute)
        obj.Drop = drop
        obj.pick = pick
        obj.transportprice = amount
        obj.save()
        return redirect('assign')

    return render(request, 'assignadd.html', {"key1": obj1, 'key2': obj2, 'key3': obj3})


def assignedit(request,id):
    obj=models.Assign.objects.get(id=id)
    obj1 = models.Busstop.objects.all()
    obj2 = models.Busroute.objects.all()
    obj3 = models.Assign.objects.all()

    if request.method == "POST":
        busstop = request.POST.get("busstop")
        busroute = request.POST.get("busroute")
        drop = request.POST.get("droptime")
        pick = request.POST.get("picktime")
        amount = request.POST.get("transportprice")

        obj = models.Assign()
        obj.busstop = models.Busstop.objects.get(id=busstop)
        obj.route = models.Busroute.objects.get(id=busroute)
        obj.Drop = drop
        obj.pick = pick
        obj.transportprice = amount
        obj.save()
        return redirect('assign')
    return render(request, 'assignedit.html', {"key1": obj1, 'key2': obj2, 'key3': obj3,'key4':obj})


def busroute(request):
    obj1 = models.Busroute.objects.all()
    obj2 = models.Busdetails.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = Busroute.objects.get(id=idd)
        obj.delete()

    return render(request, 'busroute.html', {'key1':obj1, 'key2':obj2})

def routeadd(request):

    obj1 = models.Busroute.objects.all()
    obj2 = models.Busdetails.objects.all()
    if request.method == 'POST':
        route = request.POST.get("busroute")
        busno = request.POST.get("busnumber")
        description = request.POST.get("description")

        obj = models.Busroute()
        obj.busno = models.Busdetails.objects.get(id=busno)
        obj.routename = route
        obj.desscription = description
        obj.save()
        return redirect('busroute')
    return render(request, 'routeadd.html', {'key1': obj1, 'key2': obj2})
def routeedit(request,id):
    ob  = models.Busroute.objects.get(id=id)
    obj1 = models.Busroute.objects.all()
    obj2 = models.Busdetails.objects.all()
    if request.method == 'POST':
        route = request.POST.get("busroute")
        busno = request.POST.get("busnumber")
        description = request.POST.get("description")

        ob.busno = models.Busdetails.objects.get(id=busno)
        ob.routename = route
        ob.desscription = description
        ob.save()
        return redirect('busroute')
    return render(request, 'routeedit.html', {'key1': obj1, 'key2': obj2,'key3':ob})

def fcategory(request):
    ob = Feecategory.objects.all()
    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = Feecategory.objects.get(id=idd)
        obj.delete()

    return render(request, 'fcategory.html', {'key1': ob})


def feeadd(request):
    if request.method == "POST":
        name = request.POST.get("fcategory")
        ob = models.Feecategory()
        ob.category = name
        ob.save()
        return redirect('fcategory')
    return render(request, 'feeadd.html', {})


def feeedit(request, id):
    ob = Feecategory.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get("fcategory")
        ob.category = name
        ob.save()
        return redirect('fcategory')
    return render(request, 'feeedit.html', {'key': ob})


def feetype(request):
    fee = models.Feetype.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = Feecategory.objects.get(id=idd)
        obj.delete()

    return render(request, 'feetype.html', {"key1": fee})


def typeadd(request):
    if request.method == "POST":
        type = request.POST.get("feetype")
        ob = models.Feetype()
        ob.feetype = type
        ob.save()
        return redirect('feetype')

    return render(request, 'typeadd.html', {})


def typeedit(request, id):
    ob = models.Feetype.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get("fcategory")
        ob.feetype = name
        ob.save()
        return redirect('feetype')
    return render(request, 'typeedit.html', {'key': ob})


def fsubcategory(request):
    obj1 = models.Feesubcategory.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        obj = models.Feesubcategory.objects.get(id=idd)
        obj.delete()

    return render(request, 'fsubcategory.html', {'key1': obj1})


def subadd(request):
    obj1 = models.Feecategory.objects.all()
    obj2 = models.Feetype.objects.all()

    if request.method == "POST":
        name = request.POST.get("feecategory")
        type = request.POST.get("feetype")
        amount = request.POST.get('amount')
        date = request.POST.get('fromdate')
        due = request.POST.get('duedate')

        obj = models.Feesubcategory()
        obj.category = models.Feecategory.objects.get(id=name)
        obj.feetype = models.Feetype.objects.get(id=type)
        obj.fromdate = date
        obj.Duedate = due
        obj.amount = amount
        obj.save()

        return redirect('fsubcategory')

    return render(request, 'subadd.html', {'key1': obj1, 'key2': obj2})


def subedit(request, id):
    ob = models.Feesubcategory.objects.get(id=id)
    obj1 = models.Feesubcategory.objects.all()
    if request.method == "POST":
        name = request.POST.get("category")
        type = request.POST.get("feetype")
        date = request.POST.get("fromdate")
        due = request.POST.get("duedate")
        amount = request.POST.get("amount")

        obj = models.Feesubcategory()
        obj.category = models.Feecategory.objects.get(category=name)
        obj.feetype = models.Feetype.objects.get(feetype=type)
        obj.fromdate = date
        obj.Duedate = due
        obj.amount = amount
        obj.save()
        return redirect('fsubcategory')
    return render(request, 'subedit.html', {'key': ob, 'key1': obj1})


def feeallocation(request):
    obj1 = models.Feeallocation.objects.all()

    if request.method == "POST" and 'delete' in request.POST:
        idd = request.POST.get("delete")
        obj = models.Feeallocation.objects.get(id=idd)
        obj.delete()

    return render(request, 'feeallocation.html', {'key1': obj1})

def alloedit(request,id):
    obj =models.Feeallocation.objects.get(id=id)
    obj1 = models.Feecategory.objects.all()
    obj2 = models.Feetype.objects.all()
    obj3 = models.Course.objects.all()
    if request.method == "POST":
        print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        name = request.POST.get("feecategory")
        type = request.POST.get("feetype")
        course = request.POST.get("coursename")
        amount = request.POST.get("amount")

        obj.category = models.Feecategory.objects.get(id=name)
        obj.type = models.Feetype.objects.get(id=type)
        obj.course = models.Course.objects.get(id=course)
        obj.amount = amount
        obj.Duedate = datetime.now() + timedelta(days=15)
        obj.save()

        return redirect('feeallocation')
    return render(request, 'alloedit.html', {'key1': obj1, 'key2': obj2, 'key3': obj3,'key4':obj})


def alloadd(request):
    obj1 = models.Feecategory.objects.all()
    obj2 = models.Feetype.objects.all()
    obj3 = models.Course.objects.all()
    if request.method == "POST":
        print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        name = request.POST.get("feecategory")
        type = request.POST.get("feetype")
        course = request.POST.get("coursename")
        amount = request.POST.get("amount")

        obj = models.Feeallocation()
        obj.category = models.Feecategory.objects.get(id=name)
        obj.type = models.Feetype.objects.get(id=type)
        obj.course = models.Course.objects.get(id=course)
        obj.amount = amount
        obj.Duedate = datetime.now() + timedelta(days=15)
        obj.save()

        return redirect('feeallocation')
    return render(request, 'alloadd.html', {'key1': obj1, 'key2': obj2, 'key3': obj3})


def feecollection(request, course=None, admno=None):
    obj1 = models.Course.objects.all().values()
    obj2 = models.Student.objects.all().values()
    obj3 = ''
    ob2 = ''
    ob1 = ''
    obj=''
    ob7=''
    msg=''
    balance = None
    if course and admno:
        ob = models.Student.objects.filter(AdmissionNumber=admno)
        obj3 = models.Feeallocation.objects.filter(course=course).values()

    if request.method=='POST' and 'search' in request.POST:
        academicyear = request.POST.get('academicyear')
        course = request.POST.get('coursename')
        batch = request.POST.get('batchname')
        day = request.POST.get('day')
        o = models.Academicyear.objects.get(academicyearname=academicyear)
        o1 = models.Course.objects.get(id=course)
        o2 = models.Batch.objects.get(id=batch)
        obj3 = models.Subject.objects.filter(courseid=course,academicid__isactive=True)

    obj1 = models.Academicyear.objects.get(isactive=True)
    obj2 = models.Course.objects.filter(academicid__isactive=True)
    if request.method=='POST' and 'submit' in request.POST:
        print("iiiiiiiiiiiiiiiiiiiiiiiiiii")
        academicyear = request.POST.get('academicyearid')
        course = request.POST.get('courseid')
        batch = request.POST.get('batchid')
        day = request.POST.get('day')
        print(academicyear,course,batch,day,'++++++++++++')
        for i in obj3:
            print(i)
            ob = models.Feecollection.objects.filter(fee__category_id=i['category_id'], admission_id=admno).last()
            if ob!=None:
                feecategory = models.Feecategory.objects.get(id=i['category_id'])
                feetype = models.Feetype.objects.get(id=i['type_id'])

                i['category_name'] = feecategory.category
                i['feetype_name'] = feetype.feetype
            else:
                feecategory = models.Feecategory.objects.get(id=i['category_id'])
                feetype = models.Feetype.objects.get(id=i['type_id'])
                i['category_name'] = feecategory.category
                i['feetype_name'] = feetype.feetype
                i['balance'] = i['amount']
    if request.method == 'POST' and 'submit' in request.POST:

        course = request.POST.get("coursename")
        admno = request.POST.get("admissionnumber")


        return redirect('/school/feecollection/' + str(course) + '/' + str(admno) + '/')
        ob7=models.Student.objects.get(AdmissionNumber=admno)
    ob2 = models.Student.objects.filter(course=course)

    if request.method == 'POST' and 'save' in request.POST:
        paid = request.POST.get("paid")
        category = request.POST.get('category')
        # admno = request.POST.get('admissionnumber')
        amount = request.POST.get("amount")
        ob7 = models.Feecollection.objects.filter(fee__category_id = category,admission_id=admno)
        print('hhhhhhhhhhhh',ob7,category,admno)
        if not ob7:
            print('-------reshma---------')
            obj = models.Feecollection()
            obj.course = models.Course.objects.get(id=course)
            obj.paid = paid


            if balance == None:
                obj.balance = int(amount) - int(paid)
            if balance != None:
                obj.balance = balance - int(paid)
            if obj.balance==0:
                obj.status='Paid'
            elif obj.balance< int(amount):
                obj.status='Partially Paid'
            else:
                obj.status='Unpaid'
            obj.save()
        else:
            last_fee = models.Feecollection.objects.filter(fee__category_id=category, admission=admno).last()
            last_fee.balance

def timetablemake(request):
    o=''
    o1=''
    o2=''
    day=''
    obj3=''
    obj4=''
    msg=''
      # obj1=models.Timetable.objects.filter(isactive=True)
      # obj2=models.Course.objects.all()
    if request.method=='POST' and 'search' in request.POST:
        academicyear = request.POST.get('academicyear')
        course = request.POST.get('coursename')
        batch = request.POST.get('batchname')
        day = request.POST.get('day')
        o = models.Academicyear.objects.get(academicyearname=academicyear)
        o1 = models.Course.objects.get(id=course)
        o2 = models.Batch.objects.get(id=batch)
        obj3 = models.Subject.objects.filter(courseid=course,academicid__isactive=True)

    obj1 = models.Academicyear.objects.get(isactive=True)
    obj2 = models.Course.objects.filter(academicid__isactive=True)
    if request.method=='POST' and 'submit' in request.POST:

        academicyear = request.POST.get('academicyearid')
        batch = request.POST.get('batchid')
        course = request.POST.get('courseid')
        day = request.POST.get('day')
        print (request.POST,'--------------------------------------------------------')
        try:
            for i in range(1,100):
                obj=models.Timetable()
                obj.academicyearname=models.Academicyear.objects.get(id=academicyear)
                obj.coursename=models.Course.objects.get(id=course)
                obj.batchname=models.Batch.objects.get(id=batch)
                obj.Day=day
                starttime=request.POST.get('starttime' +str(i))
                endtime=request.POST.get('endtime' + str(i))
                teacher=request.POST.get('teacher' + str(i))
                subject = request.POST.get('subject' + str(i))
                obj4=models.Timetable.objects.filter(starttime=starttime,endtime=endtime,teacher=teacher)
                if not obj4:
                    obj.starttime = starttime
                    obj.endtime = endtime
                    obj.teacher =models.Teacher.objects.get(id=teacher)
                    if request.POST.get('break' + str(i))=='on':
                        obj.isbreak = True
                    else:
                        obj.isbreak=False
                        obj.subject = models.Subject.objects.get(id=subject)
                        obj.teacher= models.Teacher.objects.get(id=teacher)
                    obj.save()
                else:
                    msg='conflict'
        except:
            print("storage running out")
    return render(request,'timetablesetting.html',{'key1':obj1,'key2':obj2,'key3':obj4,'o':o,'o1':o1,'o2':o2,'day':day,'obj3':obj3,'msg':msg})


def viewtimetable(request):
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
    return render(request,'viewtimetable.html',{'key1':obj1,'key2':obj2,'key3':obj3,'key4':obj4,'key5':obj5})

def placement(request):
    placement = models.Placement.objects.all()
    admissionyear=models.Student.objects.values('AdmissionYear').distinct()

    if request.method == 'POST' and 'add' in request.POST:
        return redirect('placementdetails')
    if request.method == 'POST' and 'submit' in request.POST:
        admissionyear=request.POST.get('admissionyear')
        filepath = 'media/placement/'
        file = request.FILES["file"]
        data = os.path.join(str(filepath), str(file))
        if os.path.isfile(data):
            os.remove(data)
        else:
            pass

        place=models.PlacementBulk()
        place.admissionyear=admissionyear
        place.uploaddata=file
        place.save()
        wb = xlrd.open_workbook(data)
        sheet = wb.sheet_by_index(0)
        row = sheet.nrows
        for i in range(1,row):

            admno = int(sheet.cell_value(i, 0))
            admyear =int(sheet.cell_value(i, 1))
            name = sheet.cell_value(i,2)
            email = sheet.cell_value(i, 3)
            mobile = int(sheet.cell_value(i,4))
            company = sheet.cell_value(i,5)
            salary = sheet.cell_value(i,6)
            print(admno, admissionyear, name, email)
            obj1=models.Placement.objects.filter(admissionno=admno, admissionyear=admyear, name=name,email=email,mobile=mobile,company=company,salary=salary)
            if not obj1:
                models.Placement.objects.create(admissionno=admno, admissionyear=admyear, name=name,email=email,mobile=mobile,company=company,salary=salary)
            else:
                pass
    if request.method=='POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.Placement.objects.get(id=idd)
        ob.delete()

    if request.method =='POST' and 'search' in request.POST:
        admissionno = request.POST.get('admissionno')
        placement = models.Placement.objects.filter(admissionno=admissionno)
    else:
        pass
    return render(request,'placement.html',{'key':admissionyear,'key1':placement})


def placementdetails(request):
    if request.method == 'POST':
        admno = request.POST.get("admissionnumber")
        admissionyear = request.POST.get("admissionyear")
        firstname = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        company = request.POST.get("company")
        salary = request.POST.get("salary")
        placement=models.Placement()
        placement.admissionno = admno
        placement.admissionyear = admissionyear
        placement.name = firstname
        placement.email = email
        placement.mobile = mobile
        placement.company = company
        placement.salary = salary
        placement.save()
        return redirect('placement')

    return render(request,'placementdetails.html',{})


def editplacement(request,id):
    key = models.Placement.objects.get(id=id)
    if request.method == 'POST':
        admno = request.POST.get("admissionnumber")
        admissionyear = request.POST.get("admissionyear")
        firstname = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        company = request.POST.get("company")
        salary = request.POST.get("salary")

        key.admissionno = admno
        key.admissionyear = admissionyear
        key.name = firstname
        key.email = email
        key.mobile = mobile
        key.company = company
        key.salary = salary
        key.save()
        return redirect('placement')
    return render(request,'editplacement.html',{'key':key})


def higherstudies(request):
    key = models.HigherStudies.objects.all()
    if request.method == 'POST' and 'add' in request.POST:
        return redirect('higherstudiesdetails')

    if request.method == 'POST' and 'submit' in request.POST:
        admissionyear = request.POST.get('admissionyear')
        file = request.FILES['file']

        filepath = 'media/higherstudies/'
        data = os.path.join(str(filepath),str(file))

        if os.path.isfile(data):
            os.remove(data)
        else:
            pass

        higher = models.HigherStudiesBulk()
        higher.admissionyear = admissionyear
        higher.data = file
        higher.save()

        wb = xlrd.open_workbook(data)
        sheet = wb.sheet_by_index(0)
        row = sheet.nrows
        for i in range(1, row):

            admno = int(sheet.cell_value(i, 0))
            admyear = int(sheet.cell_value(i, 1))
            name = sheet.cell_value(i, 2)
            email = sheet.cell_value(i, 3)
            mobile = int(sheet.cell_value(i, 4))
            rank = sheet.cell_value(i, 5)
            college = sheet.cell_value(i, 6)

            obj1 = models.HigherStudies.objects.filter(admissionno=admno, admissionyear=admyear, name=name, email=email,
                                                   mobile=mobile, entrancerank=rank, college=college)
            if not obj1:
                models.HigherStudies.objects.create(admissionno=admno, admissionyear=admyear, name=name, email=email,
                                                mobile=mobile, entrancerank=rank,college=college)
            else:
                pass
    if request.method=='POST' and 'delete' in request.POST:
        idd = request.POST.get('delete')
        ob = models.HigherStudies.objects.get(id=idd)
        ob.delete()

    if request.method =='POST' and 'search' in request.POST:
        admissionno = request.POST.get('admissionno')
        key = models.HigherStudies.objects.filter(admissionno=admissionno)
    else:
        pass
    return render(request,'higherstudies.html',{'key':key})



def higherstudiesdetails(request):

    if request.method == 'POST':
        admno = request.POST.get("admissionnumber")
        admissionyear = request.POST.get("admissionyear")
        firstname = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        rank = request.POST.get("rank")
        college = request.POST.get("college")
        higher = models.HigherStudies()
        higher.admissionno = admno
        higher.admissionyear = admissionyear
        higher.name = firstname
        higher.email = email
        higher.mobile = mobile
        higher.entrancerank = rank
        higher.college = college
        higher.save()
        return redirect('higherstudies')
    return render(request,'higherstudiesdetail.html',{})


def edithigherstudies(request,id):
    data = models.HigherStudies.objects.get(id=id)
    if request.method == 'POST':
        admno = request.POST.get("admissionnumber")
        admissionyear = request.POST.get("admissionyear")
        firstname = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        rank = request.POST.get("rank")
        college = request.POST.get("college")

        data.admissionno = admno
        data.admissionyear = admissionyear
        data.name = firstname
        data.email = email
        data.mobile = mobile
        data.entrancerank = rank
        data.college = college
        data.save()
        return redirect('higherstudies')
    return render(request,'edithigherstudies.html',{'key':data})
