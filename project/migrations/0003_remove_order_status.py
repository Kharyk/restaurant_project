# Generated by Django 4.2.16 on 2024-11-03 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_check_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
