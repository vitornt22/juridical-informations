# Generated by Django 3.2.16 on 2023-01-21 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0008_remove_part_process'),
        ('process', '0020_alter_process_forum_alter_process_judge'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='parts',
            field=models.ManyToManyField(blank=True, related_name='parts', to='parts.Part'),
        ),
    ]
