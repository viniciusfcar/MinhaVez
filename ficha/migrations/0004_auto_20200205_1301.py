# Generated by Django 2.2.7 on 2020-02-05 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ficha', '0003_auto_20200204_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]
