# Generated by Django 4.2.6 on 2023-10-27 11:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_alter_task_created_at_alter_task_created_at_week_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WeeklyTaskStats',
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 27, 11, 30, 55, 600202, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 3, 11, 30, 55, 600100, tzinfo=datetime.timezone.utc)),
        ),
    ]
