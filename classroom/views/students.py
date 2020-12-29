from datetime import date
from random import randint

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import *

from ..decorators import student_required
from ..forms import *
from ..models import *


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


@login_required
@student_required
def studentExam(request):
    today = date.today()
    upcomming_exam = Examtime.objects.all().filter(date__gt=today)
    to_take_exam = Examtime.objects.all().filter(date=today)
    outdated_exam = Examtime.objects.all().filter(date__lt=today)
    taken_exam = request.user.student.takeexam_set.all()

    for exam in taken_exam:
        to_take_exam = to_take_exam.exclude(pk=exam.exam.examtime.pk)
        outdated_exam = outdated_exam.exclude(pk=exam.exam.examtime.pk)

    students_exam = {'upcomming_exam': upcomming_exam,
                     'taken_exam': taken_exam,
                     'to_take_exam': to_take_exam,
                     'outdated_exam': outdated_exam,
                     }
    return render(request, 'classroom/students/student_comming_exam.html', students_exam)


@login_required
@student_required
def takeExam(request, pk, no_ques):
    no_ques = int(no_ques)
    examtime = get_object_or_404(Examtime, pk=pk)
    exam_set = Exam.objects.filter(examtime=examtime)
    exam_id = randint(0, len(exam_set) - 1)
    exam_code = exam_set[exam_id].code
    chosen_exam = Exam.objects.filter(examtime=examtime).get(code=exam_code)

    ques_pres = Questionpresentation.objects.filter(exam=chosen_exam)
    question_list = []
    for presentation in ques_pres:
        question_list.append(Question.objects.get(pk=presentation.question.pk))

    last_ques = "Next question"
    if no_ques < len(question_list):
        # Retrive current answer?
        question = question_list[no_ques]
        if request.method == 'POST':
            form = TakeExamForm(question=question, data=request.POST)
            if form.is_valid():
                student_choice = form.cleaned_data.get('answers')
                # Get the corresponding ques pres
                ques_pres = Questionpresentation.objects.get(exam=chosen_exam, question=question, number=no_ques + 1)
                # Get the corresponding answer
                answer_obj = Answerpart.objects.get(answerid=student_choice, question=question)

                # Create a new Answerorder
                new_answerorder = Answerorder()
                new_answerorder.answerid = answer_obj
                new_answerorder.qpresentation = ques_pres
                new_answerorder.option = student_choice

                # Delete if exists a similar answerorder:
                try:
                    todelete = Answerorder.objects.get(qpresentation=ques_pres, studentid=request.user.student)
                except Answerorder.DoesNotExist:
                    todelete = None

                if todelete:
                    todelete.delete()
                new_answerorder.studentid = request.user.student
                new_answerorder.save()

        else:
            form = TakeExamForm(question=question)

        if no_ques == len(question_list) - 1:
            last_ques = "Complete test"

        info = (no_ques + 1, question, form, examtime, last_ques, exam_id)
        context = {}
        context['info'] = info
        return render(request, "classroom/students/take_exam.html", context)

    else:
        # Save the student attempt
        new_attempt = Takeexam()
        new_attempt.student = request.user.student
        new_attempt.exam = chosen_exam
        new_attempt.save()

        messages.success(request, 'Congratulations! You completed the quiz with success!')
        return redirect('students:student_comming_exam')


@login_required
@student_required
def takeSpecificExam(request, pk, eid, no_ques):
    no_ques = int(no_ques)
    examtime = get_object_or_404(Examtime, pk=pk)
    exam_set = Exam.objects.filter(examtime=examtime)
    exam_id = int(eid)
    exam_code = exam_set[exam_id].code
    chosen_exam = Exam.objects.filter(examtime=examtime).get(code=exam_code)

    ques_pres = Questionpresentation.objects.filter(exam=chosen_exam)
    question_list = []
    for presentation in ques_pres:
        question_list.append(Question.objects.get(pk=presentation.question.pk))

    last_ques = "Next question"
    if no_ques < len(question_list):
        # Retrive current answer?
        question = question_list[no_ques]
        if request.method == 'POST':
            form = TakeExamForm(question=question, data=request.POST)
            if form.is_valid():
                student_choice = form.cleaned_data.get('answers')
                # Get the corresponding ques pres
                ques_pres = Questionpresentation.objects.get(exam=chosen_exam, question=question, number=no_ques + 1)
                # Get the corresponding answer
                answer_obj = Answerpart.objects.get(answerid=student_choice, question=question)

                # Create a new Answerorder
                new_answerorder = Answerorder()
                new_answerorder.answerid = answer_obj
                new_answerorder.qpresentation = ques_pres
                new_answerorder.option = student_choice

                # Delete if exists a similar answerorder:
                try:
                    todelete = Answerorder.objects.get(qpresentation=ques_pres, studentid=request.user.student)
                except Answerorder.DoesNotExist:
                    todelete = None

                if todelete:
                    todelete.delete()
                new_answerorder.studentid = request.user.student
                new_answerorder.save()

        else:
            form = TakeExamForm(question=question)

        if no_ques == len(question_list) - 1:
            last_ques = "Complete test"

        info = (no_ques + 1, question, form, examtime, last_ques, exam_id)
        context = {}
        context['info'] = info
        return render(request, "classroom/students/take_exam.html", context)

    else:

        # Save the student attempt
        new_attempt = Takeexam()
        new_attempt.student = request.user.student
        new_attempt.exam = chosen_exam
        new_attempt.done = True
        new_attempt.save()

        messages.success(request, 'Congratulations! You completed the quiz with success!')
        return redirect('students:student_comming_exam')


@method_decorator([login_required, student_required], name='dispatch')
class ExamResultView(DetailView):
    model = Takeexam
    template_name = 'classroom/students/view_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        takeexam = self.get_object()
        mark = 0
        context['results'] = []
        for question_presentation in takeexam.exam.questionpresentation_set.all():
            for answerorder in question_presentation.answerorder_set.all():
                if answerorder.studentid == self.request.user.student:
                    if answerorder.option == answerorder.answerid.answerid and answerorder.answerid.result == True:
                        mark = mark + 1
            class Result(object):
                pass
            result = Result()
            result.order = question_presentation.number
            result.question = question_presentation.question
            result.answer_a = question_presentation.question.answerpart_set.get(answerid='A')
            result.answer_b = question_presentation.question.answerpart_set.get(answerid='B') 
            result.answer_c = question_presentation.question.answerpart_set.get(answerid='C') 
            result.answer_d = question_presentation.question.answerpart_set.get(answerid='D')
            if len(question_presentation.answerorder_set.filter(studentid=self.request.user.student)) > 0:
                result.student_choice = question_presentation.answerorder_set.filter(studentid=self.request.user.student)[0].option
            else:
                result.student_choice = None
            context['results'].append(result)
            
        # context['question_presentations'] = takeexam.exam.questionpresentation_set.all()
        context['total'] = len(context['results'])
        context['mark'] = mark
        return context

    def get_queryset(self):
        return Takeexam.objects.all()


@method_decorator([login_required, student_required], name='dispatch')
class PastExamView(DetailView):
    model = Exam
    template_name = 'classroom/students/view_past_exam.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.get_object()
        context['results'] = []
        class Result(object):
            pass
        for question_presentation in exam.questionpresentation_set.all():
            result = Result()
            result.order = question_presentation.number
            result.question = question_presentation.question
            result.answer_a = question_presentation.question.answerpart_set.get(answerid='A')
            result.answer_b = question_presentation.question.answerpart_set.get(answerid='B') 
            result.answer_c = question_presentation.question.answerpart_set.get(answerid='C') 
            result.answer_d = question_presentation.question.answerpart_set.get(answerid='D') 
            context['results'].append(result)
            
        return context

    def get_queryset(self):
        return Exam.objects.all()