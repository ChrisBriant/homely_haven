from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.middleware import csrf
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.db import IntegrityError
#from adventcalendar.messaging import send_confirm_email, send_password_reset_email
from .forms import *
import re

def signin(request):
    #next_url = request.GET.get('next')
    form = SignInForm(request.GET)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user:
                if user.is_enabled:
                    auth_login(request,user)
                    #return HttpResponseRedirect('/calendar/mycalendars')
                else:
                    messages.error(request,'Your account is not enabled.')
                    return HttpResponseRedirect('/')
            else:
                messages.error(request,'Username or password not correct.')
                return HttpResponseRedirect('/')
        else:
            print(form.errors)
    return HttpResponseRedirect('/profile/')

def register(request):
    is_assignment_taker = True
    assignment_offerer = request.GET.get('offer')
    if assignment_offerer:
        is_assignment_taker = False
    print('offer',assignment_offerer)
    form = RegistrationForm(request.GET)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #regex
            re_pass_chk = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{10,}$'
            if re.search(re_pass_chk,form.cleaned_data['password']) and (form.cleaned_data['password'] == form.cleaned_data['passwordchk']):
                #Register user
                try:
                    user = Account.objects.create_user (form.cleaned_data['email'],form.cleaned_data['name'],form.cleaned_data['password'])
                    user.is_assignment_taker = is_assignment_taker
                    #Get joining confirmation information over to user
                    user.hash = hex(random.getrandbits(128))
                    user.save()
                    url = settings.BASE_URL + "/accounts/confirm/" + user.hash + "/"
                    #response = send_confirm_email(user.email,user.name,url)
                    messages.success(request,'Congratulations, you have successfully registered! Please check your email for the confirmation link and follow the instructions.')
                except IntegrityError as e:
                    print(e)
                    messages.error(request,'An account with this email already exists, please register with a different email address.')
            else:
                messages.error(request,'Password is invalid')
        else:
            messages.error(request,form.errors)
    return render(request,'accounts/register.html',{'form':form,'is_assignment_taker':is_assignment_taker})


def signout(request):
    next_url = request.GET.get('next')
    logout(request)
    if next_url:
        return HttpResponseRedirect(settings.BASE_URL + next_url)
    else:
        form = SignInForm()
        return render(request,'website/home.html',{'form': form,})

def confirm(request,confirm_code):
    try:
        account = Account.objects.get(hash=confirm_code)
    except Exception as e:
        return render(request,'404.html')
    account.is_enabled = True
    account.hash = ''
    account.save()
    return render(request,'accounts/confirm.html') 


def forgot(request):
    form = ForgotPasswordForm(request.GET)

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                account = Account.objects.get(email=form.cleaned_data['email'])
                account.hash = hex(random.getrandbits(128))
                account.save()
                url = settings.BASE_URL + "/accounts/reset/" + account.hash + "/"
                #send_password_reset_email(account.email,account.name,url)
                messages.success(request,'An email with a password reset link has been sent, please check your email and click on the link to change your password.')
            except Exception as e:
                return render(request,'404.html')
    return render(request,'accounts/forgot.html', {'form':form}) 


def reset(request,confirm_code):
    form = ResetPasswordForm(request.GET)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                account = Account.objects.get(hash=confirm_code)
                new_password = make_password(form.cleaned_data['password'])
                account.password = new_password
                account.hash = ''
                account.save()
                return HttpResponseRedirect('/accounts/signin')
            except Exception as e:
                messages.error(request,'An error occurred when trying to reset your password.')
        else:
            messages.error(request,form.errors)
    return render(request,'accounts/reset.html', {'form':form}) 