# Generated by Django 2.2.7 on 2020-01-26 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0002_auto_20191127_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='filas',
            field=models.ManyToManyField(blank=True, to='fila.Fila'),
        ),
    ]
