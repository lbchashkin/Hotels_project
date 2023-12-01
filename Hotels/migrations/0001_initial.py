# Generated by Django 4.2.7 on 2023-11-27 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('b_id', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('b_book_date', models.DateTimeField()),
                ('b_arr_date', models.DateField()),
                ('b_dep_date', models.DateField()),
            ],
            options={
                'db_table': 'bookings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('e_id', models.DecimalField(decimal_places=0, max_digits=6, primary_key=True, serialize=False)),
                ('e_name', models.CharField(max_length=100)),
                ('e_gender', models.CharField(max_length=1)),
                ('e_born', models.DateField()),
                ('e_phone', models.CharField(max_length=20)),
                ('e_addr', models.CharField(max_length=100)),
                ('e_mail', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('e_passp', models.CharField(max_length=11, unique=True)),
                ('e_inn', models.CharField(max_length=12, unique=True)),
                ('e_snils', models.CharField(max_length=11, unique=True)),
            ],
            options={
                'db_table': 'employees',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Filials',
            fields=[
                ('f_id', models.DecimalField(decimal_places=0, max_digits=3, primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=100, unique=True)),
                ('f_phone', models.CharField(max_length=20, unique=True)),
                ('f_addr', models.CharField(max_length=100)),
                ('f_mail', models.CharField(max_length=50, unique=True)),
                ('f_open', models.BooleanField()),
            ],
            options={
                'db_table': 'filials',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Guests',
            fields=[
                ('g_id', models.DecimalField(decimal_places=0, max_digits=6, primary_key=True, serialize=False)),
                ('g_name', models.CharField(max_length=100)),
                ('g_gender', models.CharField(max_length=1)),
                ('g_born', models.DateField()),
                ('g_phone', models.CharField(max_length=20)),
                ('g_mail', models.CharField(blank=True, max_length=50, null=True)),
                ('g_passp', models.CharField(blank=True, max_length=11, null=True, unique=True)),
            ],
            options={
                'db_table': 'guests',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('j_id', models.DecimalField(decimal_places=0, max_digits=3, primary_key=True, serialize=False)),
                ('j_name', models.CharField(max_length=100, unique=True)),
                ('j_salary', models.DecimalField(decimal_places=0, max_digits=6)),
            ],
            options={
                'db_table': 'jobs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Livings',
            fields=[
                ('l_id', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('rt_id', models.DecimalField(decimal_places=0, max_digits=2)),
                ('l_arr_date', models.DateTimeField(blank=True, null=True)),
                ('l_dep_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'livings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('r_id', models.DecimalField(decimal_places=0, max_digits=6, primary_key=True, serialize=False)),
                ('r_floor', models.DecimalField(decimal_places=0, max_digits=2)),
                ('f_id', models.DecimalField(decimal_places=0, max_digits=3)),
            ],
            options={
                'db_table': 'rooms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoomTypes',
            fields=[
                ('rt_id', models.DecimalField(decimal_places=0, max_digits=2, primary_key=True, serialize=False)),
                ('rt_price', models.DecimalField(decimal_places=0, max_digits=5)),
                ('rt_capacity', models.DecimalField(decimal_places=0, max_digits=2)),
                ('rt_area', models.DecimalField(decimal_places=0, max_digits=3)),
            ],
            options={
                'db_table': 'room_types',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoomTypesNames',
            fields=[
                ('rtn_id', models.DecimalField(decimal_places=0, max_digits=3, primary_key=True, serialize=False)),
                ('rtn_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'room_types_names',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('st_id', models.DecimalField(decimal_places=0, max_digits=2, primary_key=True, serialize=False)),
                ('st_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'statuses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('w_id', models.DecimalField(decimal_places=0, max_digits=7, primary_key=True, serialize=False)),
                ('e_hired', models.DateField()),
                ('e_fired', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'work',
                'managed': False,
            },
        ),
    ]
