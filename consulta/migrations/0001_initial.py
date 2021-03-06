# Generated by Django 2.2.5 on 2019-11-26 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('especialista', '0001_initial'),
        ('agendamento', '0001_initial'),
        ('fila', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('data', models.DateField()),
                ('create_fila', models.BooleanField()),
                ('agendamento', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agendamento.Agendamento')),
                ('especialista', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultas', to='especialista.Especialista')),
                ('filas', models.ManyToManyField(blank=True, default=None, null=True, to='fila.Fila')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
