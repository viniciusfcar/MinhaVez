# Generated by Django 3.1.3 on 2020-12-06 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responsavel', '0003_responsavel_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsavel',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_responsaveis'),
        ),
    ]
