# Generated by Django 3.1.3 on 2021-04-05 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_remove_clasedemanda_demandahabitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasedemanda',
            name='demandaHabitacion',
            field=models.CharField(default='nada', max_length=12),
            preserve_default=False,
        ),
    ]
