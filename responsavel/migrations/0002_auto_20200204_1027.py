# Generated by Django 2.2.7 on 2020-02-04 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('responsavel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsavel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
