from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import RadioSelect
from django.forms.utils import ValidationError

from classroom.models import *


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    middle_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(max_length=254)
    # address = forms.CharField(max_length=255)
    # faculty = forms.CharField(max_length=255)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user

class ExamtimeAddForm(forms.ModelForm):
    class Meta:
        model = Examtime
        fields = ['date', 'semester']

class ExamAddForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['code']



class OutcomeAddForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['outcome', 'content', 'superoutcome']

class QuestionCreateForm(forms.Form):
    question_text = forms.CharField(max_length=1000, label="Question")
    answer_text_1 = forms.CharField(max_length=1000, label="A.")
    answer_result_1 = forms.BooleanField(required=False, label="Correct ?")
    answer_text_2 = forms.CharField(max_length=1000, label="B.")
    answer_result_2 = forms.BooleanField(required=False, label="Correct ?")
    answer_text_3 = forms.CharField(max_length=1000, label="C.")
    answer_result_3 = forms.BooleanField(required=False, label="Correct ?")
    answer_text_4 = forms.CharField(max_length=1000, label="D.")
    answer_result_4 = forms.BooleanField(required=False, label="Correct ?")

class QuestionUpdateForm(forms.Form):
    question_text = forms.CharField(max_length=1000, label="Question")
    answer_text_1 = forms.CharField(max_length=1000, label="A.")
    answer_result_1 = forms.BooleanField(required=False, label="Correct ?")
    answer_text_2 = forms.CharField(max_length=1000, label="B.")
    answer_result_2 = forms.BooleanField(required=False, label="Correct ?")
    answer_text_3 = forms.CharField(max_length=1000, label="C.")
    answer_result_3 = forms.BooleanField(required=False, label="Correct ?")
    answer_text_4 = forms.CharField(max_length=1000, label="D.")
    answer_result_4 = forms.BooleanField(required=False, label="Correct ?")




class TakeExamForm(forms.Form):
    answers = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        answerA = question.answerpart_set.get(answerid='A').content.text
        answerB = question.answerpart_set.get(answerid='B').content.text
        answerC = question.answerpart_set.get(answerid='C').content.text
        answerD = question.answerpart_set.get(answerid='D').content.text

        choices = (('A', answerA),
                   ('B', answerB),
                   ('C', answerC),
                   ('D', answerD),
                   )
        print(choices)
        self.fields['answers'].choices = choices
        self.fields['answers'].widget = RadioSelect()
