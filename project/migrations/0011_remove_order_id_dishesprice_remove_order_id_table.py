# Generated by Django 4.2.16 on 2024-11-23 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_dishprice_date_alter_tableprice_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id_dishesprice',
        ),
        migrations.RemoveField(
            model_name='order',
            name='id_table',
        ),
    ]
