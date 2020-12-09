from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.
def index(request):
    users = User.objects.all().values_list()
    template = loader.get_template('exam/index.html')
    context = {
        'users': users,
    }
    return HttpResponse(template.render(context, request))
