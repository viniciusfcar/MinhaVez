# Generated by Django 2.2.7 on 2020-02-04 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fila', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fila',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]