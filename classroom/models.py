from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.core.mail import send_mail


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) 
    aim = models.TextField(blank=True, null=True)  

    class Meta:
        # managed = False
        db_table = 'Subject'

class Content(models.Model):
    text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Content'

class Outcome(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    outcome = models.CharField(max_length=10)
    content = models.CharField(max_length=500, blank=True, null=True)
    superoutcome = models.ForeignKey('self', on_delete=models.CASCADE, related_name='superoutcome_set', blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Outcome'
        unique_together = (('subject', 'outcome'),)

class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    SEX_CHOICE = [('M', 'Male'), ('F', 'Female')]
    sex = models.CharField(max_length=1, choices=SEX_CHOICE, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    class Meta:
        db_table = 'User'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, through='Teach')

    class Meta:
        # managed = False
        db_table = 'Teacher'

class Teach(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ROLE_CHOICE = [('Manager', 'Manager'), ('Main', 'Main'), ('Normal', 'Normal')]
    role = models.CharField(max_length=7, choices=ROLE_CHOICE, blank=True, null=True)
    class Meta:
        # managed = False
        db_table = 'Teach'

class Commondescription(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'CommonDescription'

class Question(models.Model):
    teacher= models.ForeignKey('Teacher', on_delete=models.CASCADE)
    modify_date = models.DateField(blank=True, null=True)
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    commondescriptions = models.ManyToManyField('Commondescription')

    class Meta:
        # managed = False
        db_table = 'Question'

class Descriptionfile(models.Model):
    path = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=50, blank=True, null=True)  
    type = models.CharField(max_length=20, blank=True, null=True)
    content = models.ManyToManyField(Content)

    class Meta:
        # managed = False
        db_table = 'DescriptionFile'

class Examtime(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    date = models.DateField()
    semester = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'ExamTime'
        unique_together = (('subject', 'date'),)

class Exam(models.Model):
    examtime = models.ForeignKey(Examtime, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    mainteacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='mainteacher_set')
    confirm_date = models.DateField(blank=True, null=True)
    manager = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='manager_set')
    check_date = models.DateField(blank=True, null=True)
    # note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Exam'
        unique_together = (('examtime', 'code'),)

class Takeexam(models.Model):
    note = models.CharField(max_length=1000, blank=True, null=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'TakeExam'

class Questionpresentation(models.Model):
    number = models.PositiveIntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'QuestionPresentation'
        unique_together = (('number', 'exam', 'question'),)


class Answerorder(models.Model):
    qpresentation = models.ForeignKey('Questionpresentation', on_delete=models.CASCADE)
    answerid = models.PositiveIntegerField()
    OPTION_CHOICE = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')]
    option = models.CharField(max_length=1, choices=OPTION_CHOICE)

    class Meta:
        # managed = False
        db_table = 'AnswerOrder'
        unique_together = (('qpresentation', 'answerid'), ('qpresentation', 'option'),)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_field = models.CharField(max_length=20, blank=True, null=True)
    yearofadmission = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    exams = models.ManyToManyField(Exam, through=Takeexam)
    answerorders = models.ManyToManyField(Answerorder)

    class Meta:
        # managed = False
        db_table = 'Student'



class Answerpart(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answerid = models.PositiveIntegerField()
    RESULT_CHOICE = [('T', 'True'), ('F', 'False')]
    result = models.CharField(max_length=1, choices=RESULT_CHOICE, blank=True, null=True)
    content = models.OneToOneField('Content', on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'AnswerPart'
        unique_together = (('question', 'answerid'),)

