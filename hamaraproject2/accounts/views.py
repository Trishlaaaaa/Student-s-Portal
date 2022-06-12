from datetime import datetime

import xlwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from tablib import Dataset
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from .genpdf import export_pdf


from .resources import StudentResource
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.contrib.staticfiles import finders
from django.views.generic import ListView
from .models import Student
from django.db import connection
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


def register(request):
    return render(request,"register.html")

def rescue(request):
    last_name = request.POST['last_name']
    first_name = request.POST['first_name']
    username= request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    if password1 == password2:
        if User.objects.filter(username=username).exists():
            # sending messages from views to page
            messages.info(request, 'Username Taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=first_name,username=username, password=password1, email=email, last_name=last_name)
            user.save();
            return redirect('login')

    else:
        messages.info(request, 'Password not matching...')
        return redirect('register')



    return render(request,"login.html")



def login(request):
    return render(request,"login.html")

def rescue2(request):
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect("main")
    else:
        messages.info(request, 'invalid credentials')
        return redirect('login')

@login_required(login_url='/login/')
def main(request):
      return render(request,'base2.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    return redirect('/')

def contact(request):

    return render(request,'contact.html')


def export(request):
    student_resource = StudentResource()
    dataset = student_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        dataset = Dataset()
        new_students = request.FILES['my_file']
        if not new_students.name.endswith('xls'):
            messages.info(request, 'Wrong Format')
            return render(request, 'upload.html')



        imported_data = dataset.load(new_students.read(), format='xls')
        # print(imported_data)
        for data in imported_data:
            value = Student(
                data[0],
                data[1],
                data[2],
                data[3],


            )
            value.save()

            # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'upload.html')

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name','EnrollNo','Branch','Section' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Student.objects.all().values_list('Name','EnrollNo','Branch','Section')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response



def dlt(request):
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE accounts_student ")
    return render(request, 'upload.html')

# def export_pdf(request):
#     buffer = io.BytesIO()
#
#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)
#
#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")
#
#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()
#
#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, filename='hello.pdf')

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        student_objs=Student.objects.all()
        # getting the template
        params={
            'student_objs':student_objs
        }
        pdf = export_pdf('result.html',params)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

#'Name','EnrollNo','DOB','Branch','Section'