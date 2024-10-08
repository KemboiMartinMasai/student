# Generated by Django 5.1 on 2024-08-13 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentApp', '0003_student_adm_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='adm_number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='enrollment_date',
            field=models.DateField(),
        ),
    ]
