# Generated by Django 3.1.3 on 2021-10-10 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0008_remove_clasereserva_demandaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasereserva',
            name='demandaId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]