# Generated by Django 3.1.3 on 2020-12-06 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0015_auto_20200522_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_usuarios'),
        ),
    ]
