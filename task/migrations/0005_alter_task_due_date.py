# Generated by Django 4.2.6 on 2023-10-27 07:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_status_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 3, 7, 28, 10, 499578, tzinfo=datetime.timezone.utc)),
        ),
    ]
