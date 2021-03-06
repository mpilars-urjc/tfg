# Generated by Django 3.1.3 on 2021-01-01 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0003_auto_20210102_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='claseApartamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartamentoIdentificador', models.CharField(max_length=5)),
                ('apartamentoPais', models.CharField(max_length=20)),
                ('apartamentoEstado', models.CharField(max_length=20)),
                ('apartamentoCiudad', models.CharField(max_length=20)),
                ('apartamentoCalle', models.CharField(max_length=40)),
                ('apartamentoNumero', models.CharField(max_length=20)),
                ('apartamentoPiso', models.CharField(max_length=20)),
                ('apartamentoLetra', models.CharField(max_length=20)),
                ('apartamentoCP', models.CharField(max_length=5)),
                ('apartamentoOtros', models.CharField(max_length=20)),
                ('apartamentoFechaDeAlta', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['apartamentoIdentificador'],
            },
        ),
    ]
