# Generated by Django 4.2.7 on 2023-12-09 03:33

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hotels', '0002_alter_bookings_options_alter_employees_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guests',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()]),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_born',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_gender',
            field=models.CharField(max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_id',
            field=models.DecimalField(decimal_places=0, max_digits=6, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_mail',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_name',
            field=models.CharField(max_length=100, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_passp',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='Номер паспорта'),
        ),
        migrations.AlterField(
            model_name='guests',
            name='g_phone',
            field=models.CharField(max_length=20, verbose_name='Телефон'),
        ),
    ]
