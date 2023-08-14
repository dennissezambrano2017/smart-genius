# Generated by Django 4.2.4 on 2023-08-14 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_alter_contenido_id_alter_material_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ejercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField()),
                ('opciones', models.JSONField()),
                ('respuesta_correcta', models.IntegerField()),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.tema')),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('puntaje', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.ejercicio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='material',
            name='contenido_material',
        ),
        migrations.RemoveField(
            model_name='material',
            name='temas',
        ),
        migrations.RemoveField(
            model_name='material',
            name='tipo',
        ),
        migrations.AddField(
            model_name='material',
            name='archivo_pdf',
            field=models.FileField(default='default.pdf', upload_to='pdfs/', validators=[tasks.models.validate_pdf_extension, tasks.models.validate_pdf_size]),
        ),
        migrations.AddField(
            model_name='material',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.tema'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Practica',
        ),
        migrations.AddField(
            model_name='material',
            name='ejercicios',
            field=models.ManyToManyField(to='tasks.ejercicio'),
        ),
    ]
