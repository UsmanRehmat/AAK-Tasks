# Generated by Django 5.1.5 on 2025-01-27 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_owner_alter_label_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(related_name='tasks', to='tasks.label'),
        ),
    ]
