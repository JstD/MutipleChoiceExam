# Generated by Django 3.1.3 on 2020-12-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_auto_20201225_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerpart',
            name='result',
            field=models.BooleanField(default=False),
        ),
    ]