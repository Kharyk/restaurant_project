# Generated by Django 4.2.16 on 2024-12-04 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_remove_order_id_dishesprice_remove_order_id_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='status',
            field=models.CharField(choices=[('Paid', 'paid'), ('Want to pay', 'wtp'), ('In process', 'not paid')], default='not paid', max_length=20),
        ),
    ]
