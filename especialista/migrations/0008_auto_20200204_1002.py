# Generated by Django 2.2.7 on 2020-02-04 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('especialista', '0007_auto_20200204_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='especializacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='especializacao.Especializacao'),
        ),
    ]
