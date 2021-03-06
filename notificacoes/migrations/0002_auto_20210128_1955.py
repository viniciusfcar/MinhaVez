# Generated by Django 3.1.4 on 2021-01-28 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificacoes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacao',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notificacao',
            name='assunto',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='notificacao',
            name='titulo',
            field=models.CharField(max_length=50),
        ),
    ]
