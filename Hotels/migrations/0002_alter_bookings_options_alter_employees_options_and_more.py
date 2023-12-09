# Generated by Django 4.2.7 on 2023-12-09 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hotels', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'managed': False, 'verbose_name': 'бронирование', 'verbose_name_plural': 'бронирования'},
        ),
        migrations.AlterModelOptions(
            name='employees',
            options={'managed': False, 'verbose_name': 'сотрудник', 'verbose_name_plural': 'сотрудники'},
        ),
        migrations.AlterModelOptions(
            name='filials',
            options={'managed': False, 'verbose_name': 'филиал', 'verbose_name_plural': 'филиалы'},
        ),
        migrations.AlterModelOptions(
            name='guests',
            options={'verbose_name': 'гость', 'verbose_name_plural': 'гости'},
        ),
        migrations.AlterModelOptions(
            name='jobs',
            options={'managed': False, 'verbose_name': 'должность', 'verbose_name_plural': 'должности'},
        ),
        migrations.AlterModelOptions(
            name='livings',
            options={'managed': False, 'verbose_name': 'проживание', 'verbose_name_plural': 'проживания'},
        ),
        migrations.AlterModelOptions(
            name='rooms',
            options={'managed': False, 'verbose_name': 'номер', 'verbose_name_plural': 'номера'},
        ),
        migrations.AlterModelOptions(
            name='roomtypes',
            options={'managed': False, 'verbose_name': 'тип номера в филиале', 'verbose_name_plural': 'типы номеров в филиалах'},
        ),
        migrations.AlterModelOptions(
            name='roomtypesnames',
            options={'managed': False, 'verbose_name': 'тип номера', 'verbose_name_plural': 'типы номеров'},
        ),
        migrations.AlterModelOptions(
            name='statuses',
            options={'managed': False, 'verbose_name': 'статус бронирования', 'verbose_name_plural': 'статусы бронирования'},
        ),
        migrations.AlterModelOptions(
            name='work',
            options={'managed': False, 'verbose_name': 'работа в филиале', 'verbose_name_plural': 'работа в филиалах'},
        ),
    ]