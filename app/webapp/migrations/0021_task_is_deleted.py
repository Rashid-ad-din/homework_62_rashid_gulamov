# Generated by Django 4.1.1 on 2022-10-14 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_alter_project_title_alter_task_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
    ]
