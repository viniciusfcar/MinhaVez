# Generated by Django 2.2.7 on 2020-05-22 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_auto_20200522_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='idNotificacao',
            new_name='notificacao',
        ),
    ]
