# Generated by Django 4.2.16 on 2024-11-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_delete_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishprice',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='tableprice',
            name='date',
            field=models.DateField(),
        ),
    ]
