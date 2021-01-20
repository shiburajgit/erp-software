"""timetableproject11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Login_view, name='login'),
    path('form/', views.Form, name='form'),
    path('admin/', views.Admin_view, name='admin'),
    path('studentadmin/', views.Studentadmin, name='studentadmin'),
    path('studentlist/',views.Studentlist, name='studentlist'),
    path('editstudent/<int:id>/',views.Editstudent, name='editstudent'),
    path('order/', views.order, name='order'),
    path('history/', views.history, name='history'),
    path('admission/', views.Admission, name='admission'),
    path('orderlist/',views.Orderlist, name='orderlist'),
    path('subject/', views.Subject, name='subject'),
    path('editsubject/<int:id>/', views.editsubject, name='editsubject'),
    path('period/', views.Period, name='period'),
    path('book/',views.book, name="book"),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('bookform/', views.bookform, name="bookform"),
    path('editbook/<int:id>/', views.editbook, name="editbook"),
    path('search/', views.search, name="search"),
    path('teacherdetails/', views.teacherdetails, name='teacherdetails'),
    path('teacherlist/', views.teacherlist, name='teacherlist'),
    path('assignteacher/',views.assignteacher,name='assignteacher'),
    path("attendanceview/",views.attendance_view,name="attendanceview"),
    path('editteacher/<int:id>/',views.editteacher,name='editteacher'),
    path('course/', views.Course_view, name="course"),
    path('editcourse/<int:id>/',views.editcourse,name='editcourse'),
    path('academicyear/',views.Academicyear, name="academicyear"),
    path('editacademicyear/<int:id>/', views.editacademicyear,name='editacademicyear'),
    path('batch/',views.Batch, name="batch"),
    path('editbatch/<int:id>/', views.editbatch, name="editbatch"),
    path('editperiod/<int:id>/',views.EditPeriod,name="editperiod"),
    path('viewtimetable/', views.viewtimetable,name='view'),
    path('setperiod/',views.timetableset,name='setperiod'),
    path('setperiod/periodselection/',views.periodselection,name='periodselection'),
    path('attendance/',views.attendance,name='attendance'),
    path('addfee/', views.addfee, name="addfee"),
    path('category/', views.category, name="category"),
    path('subcategory/',views.subcategory, name='subcategory'),
    path('report/', views.report, name='report'),
    path('transport/', views.transport, name='transport'),
    path('addtransport/', views.addtransport, name='addtransport'),
    path('edittransport/<int:id>/', views.edittransport, name="edittransport"),
    path('assign/', views.assign, name="assign"),
    path('assignadd/', views.assignadd, name="assignadd"),
    path('assignedit/<int:id>/', views.assignedit, name="assignedit"),
    path('busdetails/',views.busdetails, name='busdetails'),
    path('busadd/', views.busadd, name='busadd'),
    path('busedit/<int:id>/', views.busedit, name='busedit'),
    path('busstop/', views.busstop, name='busstop'),
    path('stopadd/', views.stopadd, name='stopadd'),
    path('stopedit/<int:id>/', views.stopedit, name='stopedit'),
    path('busroute/', views.busroute, name='busroute'),
    path('editassignteacher/<int:id>/', views.editassignteacher, name="editassignteacher"),
    path('timetablemake/', views.timetablemake, name='timetablemake'),
    path('quata/',views.quata,name='quata'),
    path('editquata/<int:id>/',views.editquata,name='editquata'),
    path('routeadd/', views.routeadd, name='routeadd'),
    path('routeedit/<int:id>', views.routeedit, name='routeedit'),
    path('fcategory/', views.fcategory, name='fcategory'),
    path('feeadd/', views.feeadd, name='feeadd'),
    path('feeedit/<int:id>/', views.feeedit, name='feeedit'),
    path('feetype/', views.feetype,name='feetype'),
    path('typeadd/', views.typeadd, name='typeadd'),
    path('typeedit/<int:id>/', views.typeedit, name='typeedit'),
    path('subadd/', views.subadd, name='subadd'),
    path('subedit/<int:id>/', views.subedit, name='subedit'),
    path('feeallocation/', views.feeallocation, name='feeallocation'),
    path('alloadd/', views.alloadd, name='alloadd'),
    path('alloedit/<int:id>/', views.alloedit, name='alloedit'),
    path('feecollection/', views.feecollection, name='feecollection'),
    path('feecollection/<int:course>/<int:admno>/', views.feecollection, name='feecollection'),
    path('placement/', views.placement,name='placement'),
    path('higherstudies/',views.higherstudies, name='higherstudies'),
    path('placementdetails/',views.placementdetails, name='placementdetails'),
    path('higherstudiesdetail/',views.higherstudiesdetails,name='higherstudiesdetails'),
    path('edithigherstudies/<int:id>/',views.edithigherstudies,name='edithigherstudies'),
    path('editplacement/<int:id>/',views.editplacement,name='editplacement'),
    path('syllabus/<int:id>/',views.syllabus,name='syllabus')
]