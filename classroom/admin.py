from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Content)
admin.site.register(Outcome)
admin.site.register(Teach)
admin.site.register(Commondescription)
admin.site.register(Question)
admin.site.register(Descriptionfile)
admin.site.register(Examtime)
admin.site.register(Exam)
admin.site.register(Takeexam)
admin.site.register(Questionpresentation)
admin.site.register(Answerorder)
admin.site.register(Answerpart)