# Generated by Django 3.1.3 on 2020-12-29 07:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('faculty', models.CharField(blank=True, max_length=255, null=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Commondescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'CommonDescription',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'Content',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('confirm_date', models.DateField(blank=True, null=True)),
                ('check_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Exam',
            },
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome', models.CharField(max_length=10)),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'Outcome',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateField(blank=True, null=True)),
                ('commondescriptions', models.ManyToManyField(blank=True, to='classroom.Commondescription')),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='classroom.content')),
                ('outcome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.outcome')),
            ],
            options={
                'db_table': 'Question',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_field', models.CharField(blank=True, max_length=20, null=True)),
                ('yearofadmission', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
            ],
            options={
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('aim', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Subject',
            },
        ),
        migrations.CreateModel(
            name='Teach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('Manager', 'Manager'), ('Main', 'Main'), ('Normal', 'Normal')], max_length=7, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.subject')),
            ],
            options={
                'db_table': 'Teach',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(blank=True, max_length=255, null=True)),
                ('subjects', models.ManyToManyField(through='classroom.Teach', to='classroom.Subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Teacher',
            },
        ),
        migrations.AddField(
            model_name='teach',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.teacher'),
        ),
        migrations.CreateModel(
            name='Takeexam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('done', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.student')),
            ],
            options={
                'db_table': 'TakeExam',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='exams',
            field=models.ManyToManyField(through='classroom.Takeexam', to='classroom.Exam'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Questionpresentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.question')),
            ],
            options={
                'db_table': 'QuestionPresentation',
                'unique_together': {('number', 'exam', 'question')},
            },
        ),
        migrations.AddField(
            model_name='question',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.teacher'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.subject'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='superoutcome',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='superoutcome_set', to='classroom.outcome'),
        ),
        migrations.CreateModel(
            name='Examtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('semester', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.subject')),
            ],
            options={
                'db_table': 'ExamTime',
                'unique_together': {('subject', 'date')},
            },
        ),
        migrations.AddField(
            model_name='exam',
            name='examtime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.examtime'),
        ),
        migrations.AddField(
            model_name='exam',
            name='mainteacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mainteacher_set', to='classroom.teacher'),
        ),
        migrations.AddField(
            model_name='exam',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_set', to='classroom.teacher'),
        ),
        migrations.CreateModel(
            name='Descriptionfile',
            fields=[
                ('path', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('content', models.ManyToManyField(to='classroom.Content')),
            ],
            options={
                'db_table': 'DescriptionFile',
            },
        ),
        migrations.AddField(
            model_name='commondescription',
            name='content',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='classroom.content'),
        ),
        migrations.CreateModel(
            name='Answerpart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerid', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('result', models.BooleanField(default=False)),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='classroom.content')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.question')),
            ],
            options={
                'db_table': 'AnswerPart',
                'unique_together': {('question', 'answerid')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='outcome',
            unique_together={('subject', 'outcome')},
        ),
        migrations.AlterUniqueTogether(
            name='exam',
            unique_together={('examtime', 'code')},
        ),
        migrations.CreateModel(
            name='Answerorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('answerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.answerpart')),
                ('qpresentation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.questionpresentation')),
                ('studentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.student')),
            ],
            options={
                'db_table': 'AnswerOrder',
                'unique_together': {('qpresentation', 'answerid'), ('qpresentation', 'option')},
            },
        ),
    ]
