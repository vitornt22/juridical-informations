# Generated by Django 3.2.16 on 2023-01-23 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0028_alter_process_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='number',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
