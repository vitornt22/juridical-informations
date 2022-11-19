# Generated by Django 4.1.3 on 2022-11-19 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=25, unique=True)),
                ('class_project', models.CharField(max_length=50)),
                ('court', models.CharField(max_length=50)),
                ('forum', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('organ', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('judge', models.CharField(max_length=50)),
                ('distribution', models.DateField(auto_now_add=True)),
                ('value', models.FloatField()),
                ('slug', models.SlugField()),
            ],
        ),
    ]
