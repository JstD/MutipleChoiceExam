from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('student', views.student, name='student'),
    # path('teacher', views.teacher, name='teacher'),
    # path('teach', views.teach, name='teach'),
    # path('subject', views.teach, name='subject'),
]