# Generated by Django 2.2.7 on 2020-04-24 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0008_auto_20200423_1802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='rua',
            new_name='logradouro',
        ),
        migrations.AddField(
            model_name='usuario',
            name='cep',
            field=models.CharField(default=2, max_length=8),
            preserve_default=False,
        ),
    ]