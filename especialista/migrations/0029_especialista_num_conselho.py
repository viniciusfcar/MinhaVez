# Generated by Django 3.1.4 on 2021-03-26 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especialista', '0028_remove_especialista_num_conselho'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialista',
            name='num_conselho',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
