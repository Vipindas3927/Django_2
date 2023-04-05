from django.shortcuts import render, redirect
from .forms import *

from .forms import *
from .models import *
from django.contrib.auth.models import User, auth
from django.http import HttpResponse

# Create your views here.

def User_Display(request):
    data = User.objects.all()
    return render(request, 'user_display.html', {'userdata': data})

def User_Register(request):
    try:
        form = User_Register_Form()
        if request.method == 'POST':
            form = User_Register_Form(request.POST)
            if form.is_valid():
                data = form.save()
                data.set_password(form.cleaned_data['password'])
                data.save()
                return User_Display(request)
        return render(request, 'user_register.html', {'form': form})
    except:
        return HttpResponse("Somthing went wrong...(error 1)")

def User_Login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return render(request, 'profile.html')
            else:
                return HttpResponse("Invalid login credentials...")
        return render(request, 'user_login.html')
    except:
        return HttpResponse("Somthing went wrong...(error 2)")

def Password_Change(request):
    try:
        if request.method == 'POST':
            user = request.POST['uname']
            old_psw = request.POST['oldpsw']
            new_psw = request.POST['newpsw']
            data = User.objects.get(username=user)
            check = data.check_password(old_psw) # checkimg thr input filed with the exsiting password
            if check == True:
                data.set_password(new_psw)
                data.save()
                print(data)
                return redirect('/login')
            else:
                return HttpResponse('Old password is wrong...')
        return render(request, 'password_change.html')
    except:
        return HttpResponse("Somthing went wrong...(error 3)")

def User_Logout(request):
    try:
        auth.logout(request)
        return User_Login(request)
    except:
        return HttpResponse("Somthing went wrong...(error 4)")
