# Generated by Django 3.2.16 on 2023-01-23 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0026_alter_process_parts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='number',
            field=models.CharField(default=32232, max_length=25, unique=True),
            preserve_default=False,
        ),
    ]