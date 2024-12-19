# Generated by Django 4.2.13 on 2024-12-19 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartOfPrivileges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(choices=[(0.9, '10%'), (0.85, '15%'), (0.7, '30%')], decimal_places=2, default=0.9, max_digits=3)),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Want to pay', 'Want to pay'), ('Current', 'Current')], default='Current', max_length=20)),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ingredients', models.TextField()),
                ('gram', models.CharField(max_length=255)),
                ('sort_daytime', models.CharField(blank=True, choices=[('Breakfast', 'breakfast'), ('Lunch', 'lunch'), ('Dinner', 'dinner')], max_length=15, null=True)),
                ('sort', models.CharField(choices=[('Appetizers', 'appetizers'), ('Main Courses', 'main'), ('Side Dishes', 'side'), ('Desserts', 'desserts'), ('Beverages', 'beverages'), ('Soups', 'soups'), ('Salads', 'salads')], max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='dish_img/')),
                ('allergies', models.ManyToManyField(to='project.allergies')),
            ],
        ),
        migrations.CreateModel(
            name='LanguageOfCommunication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number_of_people', models.IntegerField()),
                ('zone', models.CharField(choices=[('Indoors', 'indoors'), ('Outdoors', 'outdoors')], max_length=10)),
                ('sort', models.CharField(choices=[('VIP', 'vip'), ('General', 'general'), ('Appointment', 'appointment')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='table_img/')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TablePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('text', models.TextField(blank=True)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.table')),
            ],
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.CharField(choices=[('One', 'one'), ('Two', 'two'), ('Three', 'three'), ('Four', 'four'), ('Five', 'five')], max_length=5)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('id_client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.dish')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('id_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='project.check')),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_dishes', models.ManyToManyField(blank=True, to='project.dish')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraInfoUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('foto', models.ImageField(blank=True, upload_to='foto_user/')),
                ('allergies', models.ManyToManyField(to='project.allergies')),
                ('discount', models.ManyToManyField(blank=True, to='project.cartofprivileges')),
                ('language_of_communication', models.ManyToManyField(to='project.languageofcommunication')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DishPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.dish')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='comment_img/')),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.dish')),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='id_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.table'),
        ),
    ]
