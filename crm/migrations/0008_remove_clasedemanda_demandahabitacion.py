# Generated by Django 3.1.3 on 2021-04-05 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_clasedemanda_demandahabitacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clasedemanda',
            name='demandaHabitacion',
        ),
    ]
