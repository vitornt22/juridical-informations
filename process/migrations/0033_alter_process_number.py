# Generated by Django 3.2.16 on 2023-01-23 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0032_alter_process_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='number',
            field=models.CharField(default=2, max_length=25, unique=True),
            preserve_default=False,
        ),
    ]
