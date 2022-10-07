# Generated by Django 4.1.1 on 2022-10-06 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_alter_task_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.ManyToManyField(related_name='states', to='webapp.state', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.ManyToManyField(related_name='types', to='webapp.type', verbose_name='Тип'),
        ),
    ]
