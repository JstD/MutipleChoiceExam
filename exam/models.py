# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Subject(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aim = models.TextField(db_column='Aim', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Subject'

class Content(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    text = models.CharField(db_column='Text', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Content'

class Outcome(models.Model):
    subjectid = models.OneToOneField('Subject', models.DO_NOTHING, db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    outcomeid = models.PositiveIntegerField(db_column='OutcomeID', unique=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Outcome'
        unique_together = (('subjectid', 'outcomeid'),)

class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mname = models.CharField(db_column='Mname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lname = models.CharField(db_column='Lname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    faculty = models.CharField(db_column='Faculty', max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'User'

class Student(models.Model):
    id = models.OneToOneField('User', models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='class', max_length=20, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    yearofadmission = models.DecimalField(db_column='YearOfAdmission', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Student'

class Teacher(models.Model):
    id = models.OneToOneField('User', models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    degree = models.CharField(db_column='Degree', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Teacher'

class Question(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contentid = models.ForeignKey(Content, models.DO_NOTHING, db_column='ContentID')  # Field name made lowercase.
    teacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='TeacherID')  # Field name made lowercase.
    modify_date = models.DateField(db_column='Modify_date', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Outcome, models.DO_NOTHING, db_column='SubjectID')  # Field name made lowercase.
    outcomeid = models.ForeignKey(Outcome, models.DO_NOTHING, db_column='OutcomeID', related_name='outcomeid_question_set')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Question'


class Commondescription(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contentid = models.ForeignKey('Content', models.DO_NOTHING, db_column='ContentID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'CommonDescription'

class Descriptionfile(models.Model):
    path = models.CharField(db_column='Path', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'DescriptionFile'

class Examtime(models.Model):
    subjectid = models.OneToOneField('Subject', models.DO_NOTHING, db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    semester = models.DecimalField(db_column='Semester', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'ExamTime'
        unique_together = (('subjectid', 'date'),)

class Exam(models.Model):
    subjectid = models.OneToOneField('Examtime', models.DO_NOTHING, db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    date = models.ForeignKey('Examtime', models.DO_NOTHING, db_column='Date', related_name='date_exam_set')  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=10)  # Field name made lowercase.
    mainteacherid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='MainTeacherID')  # Field name made lowercase.
    confirm_date = models.DateField(db_column='Confirm_date', blank=True, null=True)  # Field name made lowercase.
    managerid = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='ManagerID', related_name='managerid_exam_set')  # Field name made lowercase.
    check_date = models.DateField(db_column='Check_date', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Exam'
        unique_together = (('subjectid', 'date', 'code'),)



class Answerpart(models.Model):
    questionid = models.OneToOneField('Question', models.DO_NOTHING, db_column='QuestionID', primary_key=True)  # Field name made lowercase.
    answerid = models.PositiveIntegerField(db_column='AnswerID')  # Field name made lowercase.
    result = models.CharField(db_column='Result', max_length=5, blank=True, null=True)  # Field name made lowercase.
    contentid = models.ForeignKey('Content', models.DO_NOTHING, db_column='ContentID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'AnswerPart'
        unique_together = (('questionid', 'answerid'),)


class Questionpresentation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    number = models.PositiveIntegerField(db_column='Number')  # Field name made lowercase.
    subjectid = models.ForeignKey(Exam, models.DO_NOTHING, db_column='SubjectID')  # Field name made lowercase.
    date = models.ForeignKey(Exam, models.DO_NOTHING, db_column='Date', related_name='date_questionpresentation_set')  # Field name made lowercase.
    code = models.ForeignKey(Exam, models.DO_NOTHING, db_column='Code', related_name='code_questionpresentation_set')  # Field name made lowercase.
    questionid = models.ForeignKey(Question, models.DO_NOTHING, db_column='QuestionID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'QuestionPresentation'
        unique_together = (('number', 'subjectid', 'date', 'code', 'questionid'),)


class Upperof(models.Model):
    outcomeid = models.OneToOneField(Outcome, models.DO_NOTHING, db_column='OutcomeID', primary_key=True, related_name='outcomeid_upperof_set')  # Field name made lowercase.
    superoutcomeid = models.ForeignKey(Outcome, models.DO_NOTHING, db_column='SuperOutcomeID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'UpperOf'

class Takeexam(models.Model):
    studentid = models.OneToOneField(Student, models.DO_NOTHING, db_column='StudentID', primary_key=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Exam, models.DO_NOTHING, db_column='SubjectID')  # Field name made lowercase.
    date = models.ForeignKey(Exam, models.DO_NOTHING, db_column='Date', related_name='date_takeexam_set')  # Field name made lowercase.
    code = models.ForeignKey(Exam, models.DO_NOTHING, db_column='Code', related_name='code_takeexam_set')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'TakeExam'
        unique_together = (('studentid', 'subjectid', 'date', 'code'),)


class Use(models.Model):
    questionid = models.OneToOneField(Question, models.DO_NOTHING, db_column='QuestionID', primary_key=True)  # Field name made lowercase.
    commondescriptionid = models.ForeignKey(Commondescription, models.DO_NOTHING, db_column='CommonDescriptionID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = '_Use'
        unique_together = (('questionid', 'commondescriptionid'),)

class Associatewith(models.Model):
    contentid = models.OneToOneField('Content', models.DO_NOTHING, db_column='ContentID', primary_key=True)  # Field name made lowercase.
    path = models.ForeignKey('Descriptionfile', models.DO_NOTHING, db_column='Path')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'AssociateWith'
        unique_together = (('contentid', 'path'),)

class Teach(models.Model):
    teacherid = models.OneToOneField('Teacher', models.DO_NOTHING, db_column='TeacherID', primary_key=True)  # Field name made lowercase.
    subjectid = models.ForeignKey(Subject, models.DO_NOTHING, db_column='SubjectID')  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Teach'
        unique_together = (('teacherid', 'subjectid'),)

class Answer(models.Model):
    studentid = models.OneToOneField('Student', models.DO_NOTHING, db_column='StudentID', primary_key=True)  # Field name made lowercase.
    qpresentationid = models.ForeignKey('Questionpresentation', models.DO_NOTHING, db_column='QPresentationID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Answer'
        unique_together = (('studentid', 'qpresentationid'),)

class Options(models.Model):
    studentid = models.OneToOneField(Answer, models.DO_NOTHING, db_column='StudentID', primary_key=True, related_name='studentid_options_set')  # Field name made lowercase.
    qpresentationid = models.ForeignKey(Answer, models.DO_NOTHING, db_column='QPresentationID')  # Field name made lowercase.
    id = models.PositiveIntegerField(db_column='ID')  # Field name made lowercase.
    field_option = models.CharField(db_column='_Option', max_length=1)  # Field name made lowercase. Field renamed because it started with '_'.

    class Meta:
        # managed = False
        db_table = 'Options'
        unique_together = (('studentid', 'qpresentationid', 'id', 'field_option'),)


class Answerorder(models.Model):
    qpresentationid = models.OneToOneField('Questionpresentation', models.DO_NOTHING, db_column='QPresentationID', primary_key=True)  # Field name made lowercase.
    id = models.PositiveIntegerField(db_column='ID')  # Field name made lowercase.
    field_option = models.CharField(db_column='_Option', max_length=1)  # Field name made lowercase. Field renamed because it started with '_'.

    class Meta:
        # managed = False
        db_table = 'AnswerOrder'
        unique_together = (('qpresentationid', 'id', 'field_option'),)

