from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import *
from django.urls import *


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            print("Kk")
            return redirect(reverse('teachers:subject_list'))
            # return HttpResponse("Student " + request.user.username + "login succesfully")
        else:
            return redirect(reverse('students:subject_list'))
            # return HttpResponse("Student" + request.user.username + "login succesfully")
    return render(request, 'classroom/home.html')
