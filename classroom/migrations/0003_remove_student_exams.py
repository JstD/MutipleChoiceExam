# Generated by Django 3.1.3 on 2020-12-29 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_remove_takeexam_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='exams',
        ),
    ]
