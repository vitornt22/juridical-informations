# Generated by Django 4.1.3 on 2022-11-20 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('process', '0009_process_jugde'),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('R', 'RÉU'), ('J', 'JUIZ'), ('A', 'AUTOR')], max_length=1)),
                ('process', models.ManyToManyField(related_name='parts', to='process.process')),
            ],
        ),
    ]
