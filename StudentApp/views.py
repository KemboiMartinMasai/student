from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,User
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from StudentApp.forms import *
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import csv
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
import datetime, csv
from django.http import HttpResponse
from datetime import datetime
import dateutil.relativedelta as delta
import dateutil.parser as parser
from django.core.files.storage import FileSystemStorage
import io
from openpyxl import Workbook
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.db import IntegrityError

from .models import *
from .forms import *
from .forms import CreateUserForm
# Create your views here.
def Home(request):
    return render(request,"index.html")


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # Use the custom form
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(username=username, password=password1)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('/handlelogin')
        else:
            # Display password validation error messages
            password_errors = form.errors.get('password1')
            if password_errors:
                for error in password_errors:
                    messages.error(request, f'Password: {error}')

            # Display general form errors
            for field, field_errors in form.errors.items():
                if field != 'password1':
                    for error in field_errors:
                        messages.error(request, f'{field}: {error}')
    else:
        form = CreateUserForm()  # Use the custom form
    return render(request,"signup.html")

def handlelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User = authenticate(request, username=username, password=password)
        if User is not None:
            login(request, User)
            messages.info(request, 'logged in successfully')
            return redirect('dashboard')
        else:
            messages.info(request, "invalid username or password")
    return render(request,"handlelogin.html")

def logout_page(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('handlelogin')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/change_password')  # URL to redirect after successful password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def add_student(request):
    error = ""
    if not request.user.is_staff:
        messages.warning(request, "Please, For Staff only!")
        return redirect('handlelogin')
    
    if request.method == 'POST':
        a = request.POST.get('adm_number')
        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        g = request.POST.get('gender')
        d = request.POST.get('date_of_birth')
        ed = request.POST.get('enrollment_date')
        e = request.POST.get('email')
        p = request.POST.get('phone_number')
        pp = request.FILES.get('profile_picture') 
           
        try:
            q = Student.objects.create(adm_number=a,first_name=f, last_name=l, gender=g, date_of_birth=d, enrollment_date=ed, email=e,phone_number=p,  profile_picture=pp)
            messages.info(request, "Student added successfully")
            return redirect('student_list')
        except IntegrityError:
            # Handle primary key violation (e.g., duplicate primary key)
            error = "Student with the same Number key already exists."       
    return render(request, 'adminlte/pages/add_student.html', {'error': error})

def student_list(request):
    if not request.user.is_staff:
        messages.warning(request, "Please, For Staff only!")
        return redirect('handlelogin')
    students = Student.objects.all()
    return render(request,'adminlte/pages/student_list.html', {'students': students})

def Delete_Student(request,pid):
    equipment = Student.objects.get(id=pid)
    equipment.delete()
    return redirect('/student_list')

def View_Student(request):
    if not request.user.is_staff:
        messages.warning(request,"Please, For Staff only!")
        return redirect('handlelogin')
    
    query = request.GET.get('query')
    stud = Student.objects.all()

    if query:
        stud = stud.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(unit__icontains=query)
            
        )
    context = {
        'stud':stud
    }
    return render(request, 'view_student.html', context)
def viewOneStudent(request, id):
    Stud = Student.objects.get(id=id)
    context = {
        "Stud": Stud
    }
    return render(request, 'viewOneStudent.html', context)

def update_student(request,adm_number):
    post = get_object_or_404(Student, adm_number=adm_number)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/student_list',id=id)
    else:
        form = StudentForm(instance=post)
    return render(request, 'update_student.html', {'form': form, 'post': post})

def viewOneStudent(request, adm_number):
    st = get_object_or_404(Student, adm_number=adm_number)
    context = {
        "st": st
    }
    return render(request, 'viewOneMember.html', context)

def dashboard (request):
    return render(request, 'adminlte/index.html')