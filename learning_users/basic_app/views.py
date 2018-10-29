from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in!!!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method=='POST':

        user_form=UserForm(data=request.POST)
        user_profile_form=UserProfileInfoForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():

            user=user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = user_profile_form.save(commit=False)
            user_profile.user=user

            if 'profile_pic' in request.FILES:
                print('Pic Uploaded')
                user_profile.profile_pic = request.FILES['profile_pic']

            user_profile.save()
            registered = True

        else:
            print('Something went wrong: ',user_form.errors,user_profile_form.errors)
    else:

        user_form=UserForm()
        user_profile_form=UserProfileInfoForm()

    return render(request,'basic_app/register.html',{
                                'user_form':user_form,
                                'user_profile_form':user_profile_form,
                                'registerd':registered
                            })


def user_login(request):

    if request.method=='POST':

        user=authenticate(username=request.POST.get('username'),password=request.POST.get('password'))

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("Invalid Username or password")
    else:
        return render(request,'basic_app/login.html')
