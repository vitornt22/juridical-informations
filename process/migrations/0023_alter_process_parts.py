# Generated by Django 3.2.16 on 2023-01-21 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0008_remove_part_process'),
        ('process', '0022_alter_process_parts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='parts',
            field=models.ManyToManyField(blank=True, related_name='parts', to='parts.Part'),
        ),
    ]
