# Generated by Django 3.1.3 on 2020-12-06 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responsavel', '0002_auto_20200204_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsavel',
            name='imagem',
            field=models.FileField(blank=True, null=True, upload_to='fotos_responsaveis'),
        ),
    ]