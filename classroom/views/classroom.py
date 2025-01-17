from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import *
from django.urls import *


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect(reverse('teachers:subject_list'))
        else:
            return redirect(reverse('students:student_comming_exam'))
    return render(request, 'classroom/home.html')
