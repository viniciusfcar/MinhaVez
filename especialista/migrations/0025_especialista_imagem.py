# Generated by Django 3.1.3 on 2020-12-06 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especialista', '0024_especialista_estado_conselho'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialista',
            name='imagem',
            field=models.FileField(blank=True, null=True, upload_to='fotos_especialistas'),
        ),
    ]