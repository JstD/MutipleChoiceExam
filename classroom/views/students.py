from datetime import date
from random import randint

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.http import *

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
        for question_presentation in takeexam.exam.questionpresentation_set.all():
            for answerorder in question_presentation.answerorder_set.all():
                if answerorder.option == answerorder.answerid.answerid and answerorder.answerid.result == True:
                    mark = mark + 1
        context['mark'] = mark
        return context

    def get_queryset(self):
        return Takeexam.objects.all()

# @method_decorator([login_required, student_required], name='dispatch')
# class StudentInterestsView(UpdateView):
#     model = Student
#     form_class = StudentInterestsForm
#     template_name = 'classroom/students/interests_form.html'
#     success_url = reverse_lazy('students:quiz_list')

#     def get_object(self):
#         return self.request.user.student

#     def form_valid(self, form):
#         messages.success(self.request, 'Interests updated with success!')
#         return super().form_valid(form)


# @method_decorator([login_required, student_required], name='dispatch')
# class QuizListView(ListView):
#      model = Examtime
#      ordering = ('name', )
#      context_object_name = 'quizzes'
#      template_name = 'classroom/students/quiz_list.html'
#
#      def get_queryset(self):
#          student = self.request.user.student
#          student_interests = student.interests.values_list('pk', flat=True)
#          taken_quizzes = student.quizzes.values_list('pk', flat=True)
#          queryset = Quiz.objects.filter(subject__in=student_interests) \
#              .exclude(pk__in=taken_quizzes) \
#              .annotate(questions_count=Count('questions')) \
#              .filter(questions_count__gt=0)
#          return queryset


# @method_decorator([login_required, student_required], name='dispatch')
# class TakenQuizListView(ListView):
#     model = TakenQuiz
#     context_object_name = 'taken_quizzes'
#     template_name = 'classroom/students/taken_quiz_list.html'

#     def get_queryset(self):
#         queryset = self.request.user.student.taken_quizzes \
#             .select_related('quiz', 'quiz__subject') \
#             .order_by('quiz__name')
#         return queryset


# @login_required
# @student_required
# def take_quiz(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk)
#     student = request.user.student

#     if student.quizzes.filter(pk=pk).exists():
#         return render(request, 'students/taken_quiz.html')

#     total_questions = quiz.questions.count()
#     unanswered_questions = student.get_unanswered_questions(quiz)
#     total_unanswered_questions = unanswered_questions.count()
#     progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
#     question = unanswered_questions.first()

#     if request.method == 'POST':
#         form = TakeQuizForm(question=question, data=request.POST)
#         if form.is_valid():
#             with transaction.atomic():
#                 student_answer = form.save(commit=False)
#                 student_answer.student = student
#                 student_answer.save()
#                 if student.get_unanswered_questions(quiz).exists():
#                     return redirect('students:take_quiz', pk)
#                 else:
#                     correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
#                     score = round((correct_answers / total_questions) * 100.0, 2)
#                     TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
#                     if score < 50.0:
#                         messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
#                     else:
#                         messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
#                     return redirect('students:quiz_list')
#     else:
#         form = TakeQuizForm(question=question)

#     return render(request, 'classroom/students/take_quiz_form.html', {
#         'quiz': quiz,
#         'question': question,
#         'form': form,
#         'progress': progress
#     })
