# Generated by Django 2.2.7 on 2020-03-29 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exame', '0001_initial'),
        ('unidadeSaude', '0002_auto_20200207_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadesaude',
            name='exames',
            field=models.ManyToManyField(blank=True, to='exame.Exame'),
        ),
    ]
