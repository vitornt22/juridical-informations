# Generated by Django 4.1.3 on 2022-11-19 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0003_process_controll'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='area',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]