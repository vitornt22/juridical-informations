# Generated by Django 4.1.3 on 2023-01-19 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0016_alter_process_court'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='subject',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
