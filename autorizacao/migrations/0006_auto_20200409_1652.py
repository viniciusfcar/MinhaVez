# Generated by Django 2.2.7 on 2020-04-09 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacao', '0005_autorizacao_verifica_agendamento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='autorizacao',
            old_name='verifica_agendamento',
            new_name='verifica',
        ),
    ]