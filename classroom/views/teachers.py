from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.http import *
from datetime import *
from json import dumps 

from ..decorators import teacher_required
from ..forms import *
from ..models import *


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:subject_list')

@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectListView(ListView):
    model = Subject
    # ordering = ('name', )
    # context_object_name = 'quizzes'
    template_name = 'classroom/teachers/subject_list.html'

    def get_queryset(self):
        queryset = self.request.user.teacher.subjects.all()
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectDetailView(DetailView):
    model = Subject
    # context_object_name = 'quiz'
    # template_name = 'classroom/teachers/quiz_results.html'
    template_name = 'classroom/teachers/subject_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        # examtimes = subject.examtime_set.all()
        # context["examtimes"] = examtimes
        # context["form"] = ExamtimeAddForm()
        return context
        # quiz = self.get_object()
        # taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        # total_taken_quizzes = taken_quizzes.count()
        # quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        # extra_context = {
        #     'taken_quizzes': taken_quizzes,
        #     'total_taken_quizzes': total_taken_quizzes,
        #     'quiz_score': quiz_score
        # }
        # kwargs.update(extra_context)
        # return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.teacher.subjects.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamtimeListView(ListView):
    model = Examtime
    # ordering = ('name', )
    # context_object_name = 'quizzes'
    template_name = 'classroom/teachers/examtime_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject"] = Subject.objects.get(pk=self.kwargs['pk'])
        context["form"] = ExamtimeAddForm()
        if self.request.user.teacher.pk == Teacher.objects.get(teach__role='Main', teach__subject=context['subject']).pk:
            context["is_main"] = True
        return context

    def get_queryset(self):
        queryset = Subject.objects.get(pk=self.kwargs['pk']).examtime_set.all()
        return queryset


@login_required
@teacher_required
def add_examtime(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = ExamtimeAddForm(request.POST)
        if form.is_valid():
            examtime = form.save(commit=False)
            examtime.subject = subject
            examtime.save()
            return redirect('teachers:examtime_list', subject.pk)
    else:
        form = ExamtimeAddForm()

    return redirect('teachers:examtime_list', subject.pk)
    # return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def delete_examtime(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        examtime_pk = request.POST["btnDelete"]
        subject.examtime_set.get(pk=examtime_pk).delete()
        return redirect('teachers:examtime_list', subject.pk)

    return redirect('teachers:examtime_list', subject.pk)
    # return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamListView(ListView):
    model = Exam
    # ordering = ('name', )
    # context_object_name = 'quizzes'
    template_name = 'classroom/teachers/exam_list.html'

    def get_context_data(self, **kwargs):
        taken_exam = []
        final_res = None
        context = super().get_context_data(**kwargs)
        context["examtime"] = get_object_or_404(Examtime, pk=self.kwargs['pk'])
        #Get student who take this examtime
        # Exams = self.queryset
        exam_set = Examtime.objects.get(pk=self.kwargs['pk']).exam_set.all()
        for exam in exam_set:
            taken_exam.append(Takeexam.objects.filter(exam=exam))

        if len(taken_exam) > 1:
            for i in range(len(taken_exam)-1):
                final_res = taken_exam[i] | taken_exam[i+1]
        elif len(taken_exam) == 1:
            final_res = taken_exam[0]

        info = []
        if final_res:
            for takeexam in final_res:
                mark = 0
                print(len(takeexam.exam.questionpresentation_set.all()))
                for question_presentation in takeexam.exam.questionpresentation_set.all():
                    for answerorder in question_presentation.answerorder_set.all():
                        if answerorder.option == answerorder.answerid.answerid and answerorder.answerid.result == True:
                            mark = mark + 1


                total = len(takeexam.exam.questionpresentation_set.all())

                score_based_10 = float(mark/total) *100 if total > 0 else 0
                taker = (takeexam, mark, total, score_based_10)

                info.append(taker)

        # context["taker"] = final_res
        context["taker"] = info
        context["form"] = ExamAddForm()
        if self.request.user.teacher.pk == Teacher.objects.get(teach__role='Main', teach__subject=context['examtime'].subject).pk:
            context["is_main"] = True
        return context

    def get_queryset(self):
        queryset = Examtime.objects.get(pk=self.kwargs['pk']).exam_set.all()
        return queryset


@login_required
@teacher_required
def add_exam(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    examtime = get_object_or_404(Examtime, pk=pk)

    if request.method == 'POST':
        form = ExamAddForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.examtime = examtime
            exam.mainteacher = Teacher.objects.get(teach__role='Main', teach__subject=examtime.subject)
            exam.manager = Teacher.objects.get(teach__role='Manager', teach__subject=examtime.subject)
            exam.confirm_date = datetime.now().strftime('%Y-%m-%d')
            exam.save()
            return redirect('teachers:exam_list', examtime.pk)
    else:
        form = ExamtimeAddForm()

    return redirect('teachers:examtime_list', examtime.pk)
    # return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def delete_exam(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    examtime = get_object_or_404(Examtime, pk=pk)

    if request.method == 'POST':
        exam_pk = request.POST["btnDelete"]
        examtime.exam_set.get(pk=exam_pk).delete()
        return redirect('teachers:exam_list', examtime.pk)

    return redirect('teachers:exam_list', examtime.pk)
    # return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class AddQuestionView(ListView):
    model = Question
    ordering = ('modify_date', )
    context_object_name = 'Questions'

    def get_queryset(self):
        queryset = Question.objects.all()
        return queryset

    def form_valid(self, form):
        question = form['question'].save(commit=False)
        answer1 = form['answer1'].save(commit=False)
        answer2 = form['answer2'].save(commit=False)
        answer3 = form['answer3'].save(commit=False)
        answer4 = form['answer4'].save(commit=False)
        #answer5 = form['answer5'].save(commit=False)
        question.teacher = self.request.user
        question.modify_date = date.today()
        answer1.question = question
        answer2.question = question
        answer3.question = question
        answer4.question = question
        #answer5.question = question
        question.save()
        answer1.save()
        answer2.save()
        answer3.save()
        answer4.save()
        #answer1.save()
        messages.success(self.request, "The question was added successfully!")
        return redirect('teacher:subject_detail', question.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamDetailView(DetailView):
    model = Exam
    # context_object_name = 'quiz'
    # template_name = 'classroom/teachers/quiz_results.html'
    template_name = 'classroom/teachers/exam_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.get_object()
        subject = exam.examtime.subject
        context["role"] = 'Normal'
        if self.request.user.teacher.pk == Teacher.objects.get(teach__role='Manager', teach__subject=subject).pk:
            context["role"] = 'Manager'
        if self.request.user.teacher.pk == Teacher.objects.get(teach__role='Main', teach__subject=subject).pk:
            context["role"] = 'Main'

        if exam.manager.user.last_name is None:
            manager_last_name = ""
        else:
            manager_last_name = exam.manager.user.last_name

        if exam.manager.user.middle_name is None:
            manager_middle_name = ""
        else:
            manager_middle_name = exam.manager.user.middle_name

        if exam.manager.user.first_name is None:
            manager_first_name = ""
        else:
            manager_first_name = exam.manager.user.first_name

        context[
            'manager_name'] =  manager_middle_name + ' ' + manager_first_name + ' ' + manager_last_name

        if exam.mainteacher.user.last_name is None:
            main_teacher_last_name = ""
        else:
            main_teacher_last_name = exam.mainteacher.user.last_name
        if exam.mainteacher.user.middle_name is None:
            main_teacher_middle_name = ""
        else:
            main_teacher_middle_name = exam.mainteacher.user.middle_name
        if exam.mainteacher.user.first_name is None:
            main_teacher_first_name = ""
        else:
            main_teacher_first_name = exam.mainteacher.user.first_name

        context[
            'main_teacher_name'] = main_teacher_first_name + ' ' + main_teacher_middle_name + ' ' + main_teacher_last_name

        # context['main_teacher_name'] = exam.mainteacher.user.last_name + ' ' + exam.mainteacher.user.middle_name + ' ' + exam.mainteacher.user.first_name
        # context['manager_name'] = exam.manager.user.last_name + ' ' + exam.manager.user.middle_name + ' ' + exam.manager.user.first_name
        return context

    def get_queryset(self):
        return Exam.objects.all()


@login_required
@teacher_required
def confirm_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        exam.confirm_date = datetime.now().strftime('%Y-%m-%d')
        exam.save()
        return redirect('teachers:exam_detail', exam.pk)

    return redirect('teachers:exam_detail', exam.pk)


@login_required
@teacher_required
def check_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        exam.check_date = datetime.now().strftime('%Y-%m-%d')
        exam.save()
        return redirect('teachers:exam_detail', exam.pk)

    return redirect('teachers:exam_detail', exam.pk)

@method_decorator([login_required, teacher_required], name='dispatch')
class OutcomeListView(ListView):
    model = Outcome
    # ordering = ('name', )
    # context_object_name = 'quizzes'
    template_name = 'classroom/teachers/outcome_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        context["subject"] = subject
        context["form"] = OutcomeAddForm()
        if self.request.user.teacher.pk == Teacher.objects.get(teach__role='Main', teach__subject=subject).pk:
            context["is_main"] = True
        else:
            context["is_main"] = False
        return context

    def get_queryset(self):
        queryset = Subject.objects.get(pk=self.kwargs['pk']).outcome_set.all()
        return queryset


@login_required
@teacher_required
def add_outcome(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = OutcomeAddForm(request.POST)
        if form.is_valid():
            outcome = form.save(commit=False)
            outcome.subject = subject
            outcome.save()
            return redirect('teachers:outcome_list', subject.pk)
    else:
        form = OutcomeAddForm()

    return redirect('teachers:outcome_list', subject.pk)


@login_required
@teacher_required
def delete_outcome(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        outcome_pk = request.POST["btnDelete"]
        subject.outcome_set.get(pk=outcome_pk).delete()
        return redirect('teachers:outcome_list', subject.pk)

    return redirect('teachers:outcome_list', subject.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionListView(ListView):
    model = Question
    # ordering = ('name', )
    # context_object_name = 'questions'
    template_name = 'classroom/teachers/question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["outcome"] = get_object_or_404(Outcome, pk=self.kwargs['pk'])
        # context["form"] = QuestionCreateForm()
        return context

    def get_queryset(self):
        #queryset = Outcome.objects.get(pk=self.kwargs['pk']).question_set.all()
        queryset = Outcome.objects.get(pk=self.kwargs['pk']).question_set.all()
        # ans_set = Answerpart.objects.all()
        # queryset = {'ques_set': ques_set, 'ans_set': ans_set}
        return queryset
        #return queryset

@login_required
@teacher_required
def create_question_form(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)
    form = QuestionCreateForm()
    return render(request, 'classroom/teachers/question_create_form.html', {'outcome':outcome, 'form':form})

@login_required
@teacher_required
def create_question(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)

    if request.method == 'POST':
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            # Create content
            question_content = Content.objects.create(text=form.cleaned_data['question_text'])
            answer_content_1 = Content.objects.create(text=form.cleaned_data['answer_text_1'])
            answer_content_2 = Content.objects.create(text=form.cleaned_data['answer_text_2'])
            answer_content_3 = Content.objects.create(text=form.cleaned_data['answer_text_3'])
            answer_content_4 = Content.objects.create(text=form.cleaned_data['answer_text_4'])
            # question = form.save(commit=False)
            # Create quesion
            teacher = request.user.teacher
            modify_date = datetime.now().strftime('%Y-%m-%d')
            question = Question.objects.create(teacher=teacher, modify_date=modify_date, outcome=outcome, content=question_content)
            # Create answerpart
            Answerpart.objects.create(question=question, answerid='A', result=form.cleaned_data['answer_result_1'], content=answer_content_1)
            Answerpart.objects.create(question=question, answerid='B', result=form.cleaned_data['answer_result_2'], content=answer_content_2)
            Answerpart.objects.create(question=question, answerid='C', result=form.cleaned_data['answer_result_3'], content=answer_content_3)
            Answerpart.objects.create(question=question, answerid='D', result=form.cleaned_data['answer_result_4'], content=answer_content_4)
            return redirect('teachers:question_list', outcome.pk)
    else:
        form = QuestionCreateForm()

    return redirect('teachers:question_list', outcome.pk)


@login_required
@teacher_required
def delete_question(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)

    if request.method == 'POST':
        question_pk = request.POST["btnDelete"]
        Question.objects.get(pk=question_pk).delete()
        return redirect('teachers:question_list', outcome.pk)

    return redirect('teachers:question_list', outcome.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDetailView(DetailView):
    model = Question
    # context_object_name = 'quiz'
    # template_name = 'classroom/teachers/quiz_results.html'
    template_name = 'classroom/teachers/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answer_a'] = question.answerpart_set.get(answerid='A') 
        context['answer_b'] = question.answerpart_set.get(answerid='B') 
        context['answer_c'] = question.answerpart_set.get(answerid='C') 
        context['answer_d'] = question.answerpart_set.get(answerid='D')
        context['form'] = QuestionUpdateForm(initial={
            'question_text': question.content.text,
            'answer_text_1': question.answerpart_set.get(answerid='A').content.text,
            'answer_text_2': question.answerpart_set.get(answerid='B').content.text,
            'answer_text_3': question.answerpart_set.get(answerid='C').content.text,
            'answer_text_4': question.answerpart_set.get(answerid='D').content.text,
            'answer_result_1': question.answerpart_set.get(answerid='A').result,
            'answer_result_2': question.answerpart_set.get(answerid='B').result,
            'answer_result_3': question.answerpart_set.get(answerid='C').result,
            'answer_result_4': question.answerpart_set.get(answerid='D').result,
        })
        if question.teacher.user.last_name is None:
            teacher_last_name = ""
        else:
            teacher_last_name = question.teacher.user.last_name
        if question.teacher.user.middle_name is None:
            teacher_middle_name = ""
        else:
            teacher_middle_name = question.teacher.user.middle_name
        if question.teacher.user.first_name is None:
            teacher_first_name = ""
        else:
            teacher_first_name = question.teacher.user.first_name

        context[
            'teacher_name'] = teacher_first_name + ' ' + teacher_middle_name + ' ' + teacher_last_name
        # context['teacher_name'] = question.teacher.user.last_name + ' ' + question.teacher.user.middle_name + ' ' + question.teacher.user.first_name
        return context

    def get_queryset(self):
        return Question.objects.all()

@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionBankView(ListView):
    model = Question
    # ordering = ('name', )
    context_object_name = 'questions'
    template_name = 'classroom/teachers/question_bank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exam"] = get_object_or_404(Exam, pk=self.kwargs['pk'])
        if self.request.user.teacher.pk == Teacher.objects.get(teach__role='Main', teach__subject=context['exam'].examtime.subject).pk:
            context["is_main"] = True
        # context["form"] = QuestionCreateForm()
        return context

    def get_queryset(self):
        #queryset = Outcome.objects.get(pk=self.kwargs['pk']).question_set.all()
        exam = get_object_or_404(Exam, pk=self.kwargs['pk'])
        subject = exam.examtime.subject
        subject_outcome = Outcome.objects.filter(subject=subject)
        # print(exam)
        # queryset = Question.objects.filter(questionpresentation__exam=exam)
        question_bank = Question.objects.filter(outcome__in=subject_outcome)
        question_in_exam = Question.objects.filter(questionpresentation__exam=exam)
        queryset = {'question_bank': question_bank, 'question_in_exam': question_in_exam}
        # ans_set = Answerpart.objects.all()
        # queryset = {'ques_set': ques_set, 'ans_set': ans_set}
        return queryset

@login_required
@teacher_required
def addQuestionToExam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        question_pk = request.POST['btnAdd']
        question = Question.objects.get(pk=question_pk)
        if Questionpresentation.objects.filter(exam=exam):
            max_exam_number = Questionpresentation.objects.filter(exam=exam).latest('number').number
        else:
            max_exam_number = 0
        new_presentation = Questionpresentation()
        new_presentation.exam = exam
        new_presentation.number = max_exam_number + 1
        new_presentation.question = question
        new_presentation.save()

    return redirect('teachers:question_bank', exam.pk)

@login_required
@teacher_required
def deleteQuestionFromExam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        question_pk = request.POST['btnDelete']
        question = Question.objects.get(pk=question_pk)
        Questionpresentation.objects.filter(exam=exam, question=question).latest('number').delete()

    return redirect('teachers:question_bank', exam.pk)

@login_required
@teacher_required
def update_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            if request.user.teacher.pk == question.teacher.pk:
                answer_a = question.answerpart_set.get(answerid='A')
                answer_a.content.text = form.cleaned_data['answer_text_1']
                answer_a.result = form.cleaned_data['answer_result_1']
                answer_a.content.save()
                answer_a.save()

                answer_b = question.answerpart_set.get(answerid='B')
                answer_b.content.text = form.cleaned_data['answer_text_2']
                answer_b.result = form.cleaned_data['answer_result_2']
                answer_b.content.save()
                answer_b.save()

                answer_c = question.answerpart_set.get(answerid='C')
                answer_c.content.text = form.cleaned_data['answer_text_3']
                answer_c.result = form.cleaned_data['answer_result_3']
                answer_c.content.save()
                answer_c.save()

                answer_d = question.answerpart_set.get(answerid='D')
                answer_d.content.text = form.cleaned_data['answer_text_4']
                answer_d.result = form.cleaned_data['answer_result_4']
                answer_d.content.save()
                answer_d.save()

                question.content.text = form.cleaned_data['question_text']
                question.modify_date = datetime.now().strftime('%Y-%m-%d')
                question.content.save()
                question.save()
            return redirect('teachers:question_detail', question.pk)
    else:
        form = QuestionCreateForm()

    return redirect('teachers:question_detail', question.pk)


# @login_required
# @teacher_required
# def delete_examtime(request, pk):
#     # By filtering the quiz by the url keyword argument `pk` and
#     # by the owner, which is the logged in user, we are protecting
#     # this view at the object-level. Meaning only the owner of
#     # quiz will be able to add questions to it.
#     subject = get_object_or_404(Subject, pk=pk)

#     if request.method == 'POST':
#         examtime_pk = request.POST["btnDelete"]
#         subject.examtime_set.get(pk=examtime_pk).delete()
#         return redirect('teachers:examtime_list', subject.pk)

#     return redirect('teachers:examtime_list', subject.pk)
#     # return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})

# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizListView(ListView):
#     model = Quiz
#     ordering = ('name', )
#     context_object_name = 'quizzes'
#     template_name = 'classroom/teachers/quiz_change_list.html'

#     def get_queryset(self):
#         queryset = self.request.user.quizzes \
#             .select_related('subject') \
#             .annotate(questions_count=Count('questions', distinct=True)) \
#             .annotate(taken_count=Count('taken_quizzes', distinct=True))
#         return queryset


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizCreateView(CreateView):
#     model = Quiz
#     fields = ('name', 'subject', )
#     template_name = 'classroom/teachers/quiz_add_form.html'

#     def form_valid(self, form):
#         quiz = form.save(commit=False)
#         quiz.owner = self.request.user
#         quiz.save()
#         messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
#         return redirect('teachers:quiz_change', quiz.pk)


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizUpdateView(UpdateView):
#     model = Quiz
#     fields = ('name', 'subject', )
#     context_object_name = 'quiz'
#     template_name = 'classroom/teachers/quiz_change_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
#         return super().get_context_data(**kwargs)

#     def get_queryset(self):
#         '''
#         This method is an implicit object-level permission management
#         This view will only match the ids of existing quizzes that belongs
#         to the logged in user.
#         '''
#         return self.request.user.quizzes.all()

#     def get_success_url(self):
#         return reverse('teachers:quiz_change', kwargs={'pk': self.object.pk})


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizDeleteView(DeleteView):
#     model = Quiz
#     context_object_name = 'quiz'
#     template_name = 'classroom/teachers/quiz_delete_confirm.html'
#     success_url = reverse_lazy('teachers:quiz_change_list')

#     def delete(self, request, *args, **kwargs):
#         quiz = self.get_object()
#         messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
#         return super().delete(request, *args, **kwargs)

#     def get_queryset(self):
#         return self.request.user.quizzes.all()


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuizResultsView(DetailView):
#     model = Quiz
#     context_object_name = 'quiz'
#     template_name = 'classroom/teachers/quiz_results.html'

#     def get_context_data(self, **kwargs):
#         quiz = self.get_object()
#         taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
#         total_taken_quizzes = taken_quizzes.count()
#         quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
#         extra_context = {
#             'taken_quizzes': taken_quizzes,
#             'total_taken_quizzes': total_taken_quizzes,
#             'quiz_score': quiz_score
#         }
#         kwargs.update(extra_context)
#         return super().get_context_data(**kwargs)

#     def get_queryset(self):
#         return self.request.user.quizzes.all()


# @login_required
# @teacher_required
# def question_add(request, pk):
#     # By filtering the quiz by the url keyword argument `pk` and
#     # by the owner, which is the logged in user, we are protecting
#     # this view at the object-level. Meaning only the owner of
#     # quiz will be able to add questions to it.
#     quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.quiz = quiz
#             question.save()
#             messages.success(request, 'You may now add answers/options to the question.')
#             return redirect('teachers:question_change', quiz.pk, question.pk)
#     else:
#         form = QuestionForm()

#     return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


# @login_required
# @teacher_required
# def question_change(request, quiz_pk, question_pk):
#     # Simlar to the `question_add` view, this view is also managing
#     # the permissions at object-level. By querying both `quiz` and
#     # `question` we are making sure only the owner of the quiz can
#     # change its details and also only questions that belongs to this
#     # specific quiz can be changed via this url (in cases where the
#     # user might have forged/player with the url params.
#     quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
#     question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

#     AnswerFormSet = inlineformset_factory(
#         Question,  # parent model
#         Answer,  # base model
#         formset=BaseAnswerInlineFormSet,
#         fields=('text', 'is_correct'),
#         min_num=2,
#         validate_min=True,
#         max_num=10,
#         validate_max=True
#     )

#     if request.method == 'POST':
#         form = QuestionForm(request.POST, instance=question)
#         formset = AnswerFormSet(request.POST, instance=question)
#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 form.save()
#                 formset.save()
#             messages.success(request, 'Question and answers saved with success!')
#             return redirect('teachers:quiz_change', quiz.pk)
#     else:
#         form = QuestionForm(instance=question)
#         formset = AnswerFormSet(instance=question)

#     return render(request, 'classroom/teachers/question_change_form.html', {
#         'quiz': quiz,
#         'question': question,
#         'form': form,
#         'formset': formset
#     })


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuestionDeleteView(DeleteView):
#     model = Question
#     context_object_name = 'question'
#     template_name = 'classroom/teachers/question_delete_confirm.html'
#     pk_url_kwarg = 'question_pk'

#     def get_context_data(self, **kwargs):
#         question = self.get_object()
#         kwargs['quiz'] = question.quiz
#         return super().get_context_data(**kwargs)

#     def delete(self, request, *args, **kwargs):
#         question = self.get_object()
#         messages.success(request, 'The question %s was deleted with success!' % question.text)
#         return super().delete(request, *args, **kwargs)

#     def get_queryset(self):
#         return Question.objects.filter(quiz__owner=self.request.user)

#     def get_success_url(self):
#         question = self.get_object()
#         return reverse('teachers:quiz_change', kwargs={'pk': question.quiz_id})
