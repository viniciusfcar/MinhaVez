# Generated by Django 3.1.4 on 2020-12-10 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0016_auto_20201206_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cep',
            field=models.CharField(max_length=9),
        ),
    ]
