# Generated by Django 3.1.4 on 2021-01-26 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificacoes', '0001_initial'),
        ('usuario', '0019_auto_20210119_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='notificacoes',
            field=models.ManyToManyField(blank=True, to='notificacoes.Notificacao'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='notificacao',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
