# Generated by Django 4.2.13 on 2024-10-30 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='id_order',
            field=models.ManyToManyField(blank=True, to='project.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id_dishes',
            field=models.ManyToManyField(blank=True, to='project.dish'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id_table',
            field=models.ManyToManyField(blank=True, to='project.table'),
        ),
    ]
