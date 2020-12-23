from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import *


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            # return redirect('teachers:quiz_change_list')
            return HttpResponse("Student " + request.user.username + "login succesfully")
        else:
            # return redirect('students:quiz_list')
            return HttpResponse("Teacher" + request.user.username + "login succesfully")
    return render(request, 'classroom/home.html')
