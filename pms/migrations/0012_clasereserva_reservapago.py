# Generated by Django 3.1.3 on 2021-11-01 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0011_clasepagos'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasereserva',
            name='reservaPago',
            field=models.IntegerField(default=0),
        ),
    ]
