# Generated by Django 2.2.7 on 2020-02-04 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ficha', '0002_ficha_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuario.Usuario'),
        ),
    ]
