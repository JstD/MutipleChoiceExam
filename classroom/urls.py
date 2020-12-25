from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        # path('', students.QuizListView.as_view(), name='quiz_list'),
        # path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        # path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        # path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
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
        path('exam/<pk>/confirm', teachers.confirm_exam, name='confirm_exam'),
        path('exam/<pk>/check', teachers.check_exam, name='check_exam'),
        # path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        # path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        # path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        # path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        # path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
