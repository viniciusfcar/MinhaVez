# Generated by Django 2.2.7 on 2020-04-18 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especialista', '0016_auto_20200417_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='conselho',
            field=models.CharField(choices=[('CRM', 'CRM'), ('CRO', 'CRO'), ('CRN', 'CRN'), ('CREFITO', 'CREFITO'), ('CRFa', 'CRFa'), ('CRP', 'CRP')], max_length=20),
        ),
    ]
