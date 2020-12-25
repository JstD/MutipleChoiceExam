from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from betterforms.multiform import MultiModelForm

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

<<<<<<< HEAD
class OneQuestionAddForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content', 'commondescriptions']


class DescriptionAddForm(forms.ModelForm):
    class Meta:
        model = Commondescription

class AnswerPartAddForm(forms.ModelForm):
    class Meta:
        model = Answerpart
        fields = ['result', 'content']

class QuestionAddForm(MultiModelForm):
    form_classes = {
        'question': OneQuestionAddForm,
        'answer1': AnswerPartAddForm,
        'answer2': AnswerPartAddForm,
        'answer3': AnswerPartAddForm,
        'answer4': AnswerPartAddForm,
        'answer5': AnswerPartAddForm,
    }

class OutcomeAddForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['outcome', 'content', 'superoutcome']


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
