from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import *


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_teacher = True
    #     if commit:
    #         user.save()
    #     return user
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Subject.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        # student.interests.add(*self.cleaned_data.get('interests'))
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

# class StudentInterestsForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ('interests', )
#         widgets = {
#             'interests': forms.CheckboxSelectMultiple
#         }


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ('text', )


# class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         super().clean()

#         has_one_correct_answer = False
#         for form in self.forms:
#             if not form.cleaned_data.get('DELETE', False):
#                 if form.cleaned_data.get('is_correct', False):
#                     has_one_correct_answer = True
#                     break
#         if not has_one_correct_answer:
#             raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


# class TakeQuizForm(forms.ModelForm):
#     answer = forms.ModelChoiceField(
#         queryset=Answer.objects.none(),
#         widget=forms.RadioSelect(),
#         required=True,
#         empty_label=None)

#     class Meta:
#         model = StudentAnswer
#         fields = ('answer', )

#     def __init__(self, *args, **kwargs):
#         question = kwargs.pop('question')
#         super().__init__(*args, **kwargs)
#         self.fields['answer'].queryset = question.answers.order_by('text')
