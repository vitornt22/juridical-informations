# Generated by Django 4.1.3 on 2022-11-19 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_alter_process_distribution_alter_process_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
