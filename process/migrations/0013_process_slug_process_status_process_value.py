# Generated by Django 4.1.3 on 2022-11-20 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0012_remove_process_slug_remove_process_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='value',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]
