# Generated by Django 4.2.16 on 2024-10-31 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='id_table',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='project.table'),
        ),
    ]
