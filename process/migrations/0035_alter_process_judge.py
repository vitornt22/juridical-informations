# Generated by Django 3.2.16 on 2023-01-28 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0003_remove_judge_cnj'),
        ('process', '0034_alter_process_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='judge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='judge.judge'),
        ),
    ]
