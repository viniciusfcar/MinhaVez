# Generated by Django 2.2.7 on 2020-04-17 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especialista', '0012_especialista_conselho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='conselho',
            field=models.CharField(max_length=20),
        ),
    ]