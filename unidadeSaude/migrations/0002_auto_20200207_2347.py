# Generated by Django 2.2.7 on 2020-02-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unidadeSaude', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadesaude',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='unidadesaude',
            name='telefone',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
