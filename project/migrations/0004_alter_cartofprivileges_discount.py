# Generated by Django 4.2.13 on 2024-12-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_cartofprivileges_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartofprivileges',
            name='discount',
            field=models.DecimalField(choices=[('10', '10'), ('15', '15'), ('30', '30')], decimal_places=2, default='10%', max_digits=3),
        ),
    ]