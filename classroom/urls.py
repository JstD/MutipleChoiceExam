from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),
    path('students/', include(([
        path('', students.studentExam, name='student_comming_exam'),
        path('takeexam/(?P<pk>\w+)/(?P<no_ques>\[0-9]+)/', students.takeExam, name='student_take_exam'),
        path('takeexam/<pk>/result', students.ExamResultView.as_view(), name='view_result'),
        path('pastexam/<pk>/', students.PastExamView.as_view(), name='view_past_exam')
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.SubjectListView.as_view(), name='subject_list'),
        path('subject/<pk>/', teachers.SubjectDetailView.as_view(), name='subject_detail'),
        path('subject/<pk>/examtimes', teachers.ExamtimeListView.as_view(), name='examtime_list'),
        path('subject/<pk>/examtimes/add', teachers.add_examtime, name='add_examtime'),
        path('subject/<pk>/examtimes/delete', teachers.delete_examtime, name='delete_examtime'),
        path('examtime/<pk>/exams/', teachers.ExamListView.as_view(), name='exam_list'),
        path('examtime/<pk>/exams/add', teachers.add_exam, name='add_exam'),
        path('examtime/<pk>/exams/delete', teachers.delete_exam, name='delete_exam'),
        path('exam/<pk>/', teachers.ExamDetailView.as_view(), name='exam_detail'),
        path('exam/<pk>/questions', teachers.QuestionBankView.as_view(), name='question_bank'),
        path('exam/<pk>/questions/add', teachers.addQuestionToExam, name='add_question_to_exam'),
        path('exam/<pk>/questions/delete', teachers.deleteQuestionFromExam, name='delete_question_from_exam'),
        path('exam/<pk>/confirm', teachers.confirm_exam, name='confirm_exam'),
        path('exam/<pk>/check', teachers.check_exam, name='check_exam'),
        path('subject/<pk>/outcomes', teachers.OutcomeListView.as_view(), name='outcome_list'),
        path('subject/<pk>/outcomes/add', teachers.add_outcome, name='add_outcome'),
        path('subject/<pk>/outcomes/delete', teachers.delete_outcome, name='delete_outcome'),
        path('outcome/<pk>/questions/', teachers.QuestionListView.as_view(), name='question_list'),
        path('outcome/<pk>/questions/add/form', teachers.create_question_form, name='create_question_form'),
        path('outcome/<pk>/questions/add', teachers.create_question, name='create_question'),
        path('outcome/<pk>/questions/delete', teachers.delete_question, name='delete_question'),
        path('question/<pk>/', teachers.QuestionDetailView.as_view(), name='question_detail'),
        path('question/<pk>/update', teachers.update_question, name='update_question'),
    ], 'classroom'), namespace='teachers')),
]
