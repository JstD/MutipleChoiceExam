# Generated by Django 3.1.3 on 2020-12-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0005_auto_20201225_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='commondescriptions',
            field=models.ManyToManyField(blank=True, null=True, to='classroom.Commondescription'),
        ),
    ]
