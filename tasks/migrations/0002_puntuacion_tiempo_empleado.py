# Generated by Django 4.2.4 on 2023-08-29 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntuacion',
            name='tiempo_empleado',
            field=models.CharField(default='00:01:25', max_length=20),
        ),
    ]
