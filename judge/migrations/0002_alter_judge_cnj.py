# Generated by Django 4.1.3 on 2022-11-29 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='cnj',
            field=models.CharField(max_length=25),
        ),
    ]