# Generated by Django 4.1.3 on 2022-11-19 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='judge',
        ),
    ]