# Generated by Django 4.2.6 on 2023-10-26 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_category_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 2, 10, 50, 54, 341386, tzinfo=datetime.timezone.utc)),
        ),
    ]
