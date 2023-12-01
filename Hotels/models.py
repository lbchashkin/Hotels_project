# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bookings(models.Model):
    b_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0, verbose_name="ID")
    b_book_date = models.DateTimeField(verbose_name="Дата бронирования")
    rt = models.ForeignKey('RoomTypes', models.DO_NOTHING, verbose_name="Тип номера")
    g = models.ForeignKey('Guests', models.DO_NOTHING, verbose_name="Гость")
    b_arr_date = models.DateField(verbose_name="Дата заезда")
    b_dep_date = models.DateField(verbose_name="Дата выезда")
    st = models.ForeignKey('Statuses', models.DO_NOTHING, verbose_name="Статус бронирования")

    def __str__(self):
        return str(self.g.g_name) + "-" + self.rt.rtn.rtn_name + " от " + self.b_book_date.strftime("%H:%M %d-%m-%Y")

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'бронирования'
        managed = False
        db_table = 'bookings'
        unique_together = (('b_id', 'rt'),)


class Employees(models.Model):
    e_id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0, verbose_name='ID')
    e_name = models.CharField(max_length=100, verbose_name='Имя')
    e_gender = models.CharField(max_length=1, verbose_name='Пол')
    e_born = models.DateField(verbose_name='Дата рождения')
    e_phone = models.CharField(max_length=20, verbose_name='Телефон')
    e_addr = models.CharField(max_length=100, verbose_name='Адрес')
    e_mail = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name='Email')
    e_passp = models.CharField(unique=True, max_length=11, verbose_name='Номер паспорта')
    e_inn = models.CharField(unique=True, max_length=12, verbose_name='ИНН')
    e_snils = models.CharField(unique=True, max_length=11, verbose_name='СНИЛС')

    def __str__(self):
        return self.e_name + "_" + str(self.e_id)

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        managed = False
        db_table = 'employees'


class Filials(models.Model):
    f_id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, verbose_name='ID')
    f_name = models.CharField(unique=True, max_length=100, verbose_name='Название')
    f_phone = models.CharField(unique=True, max_length=20, verbose_name='Телефон')
    f_addr = models.CharField(max_length=100, verbose_name='Адрес')
    f_mail = models.CharField(unique=True, max_length=50, verbose_name='Email')
    f_open = models.BooleanField(verbose_name='Открыт')

    def __str__(self):
        return self.f_name

    class Meta:
        verbose_name = 'филиал'
        verbose_name_plural = 'филиалы'
        managed = False
        db_table = 'filials'


class Guests(models.Model):
    g_id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0, verbose_name='ID')
    g_name = models.CharField(max_length=100, verbose_name='ФИО')
    g_gender = models.CharField(max_length=1, verbose_name='Пол')
    g_born = models.DateField(verbose_name='Дата рождения')
    g_phone = models.CharField(max_length=20, verbose_name='Телефон')
    g_mail = models.CharField(max_length=50, blank=True, null=True, verbose_name='Email')
    g_passp = models.CharField(unique=True, max_length=11, blank=True, null=True, verbose_name='Номер паспорта')
    w = models.ForeignKey('Work', models.DO_NOTHING, blank=True, null=True, verbose_name='Сотрудник (регистрация)')

    def __str__(self):
        return self.g_name + "_" + str(self.g_id)

    class Meta:
        verbose_name = 'гость'
        verbose_name_plural = 'гости'
        managed = False
        db_table = 'guests'


class Jobs(models.Model):
    j_id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, verbose_name='ID')
    j_name = models.CharField(unique=True, max_length=100, verbose_name='Должность')
    j_salary = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Зарплата')

    def __str__(self):
        return self.j_name

    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = 'должности'
        managed = False
        db_table = 'jobs'


class Livings(models.Model):
    l_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0, verbose_name='ID')
    b = models.ForeignKey(Bookings, models.DO_NOTHING, blank=True, null=True, verbose_name='Бронирование')
    rt = models.ForeignKey('RoomTypes', models.DO_NOTHING, verbose_name='Тип номера')
    r = models.ForeignKey('Rooms', models.DO_NOTHING, blank=True, null=True, verbose_name='Номер')
    g = models.ForeignKey(Guests, models.DO_NOTHING, verbose_name='Гость')
    w_id_arr = models.ForeignKey('Work', models.DO_NOTHING, db_column='w_id_arr', blank=True, null=True, verbose_name='Сотрудник (заселение)')
    l_arr_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата заселения')
    w_id_dep = models.ForeignKey('Work', models.DO_NOTHING, db_column='w_id_dep', related_name='livings_w_id_dep_set',
                                 blank=True, null=True, verbose_name='Сотрудник (выселение)')
    l_dep_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата выселения')

    def __str__(self):
        return self.g.g_name + " " + self.rt.rtn.rtn_name + f" {self.l_arr_date.strftime('%d.%m.%Y')} - {self.l_dep_date.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = 'проживание'
        verbose_name_plural = 'проживания'
        managed = False
        db_table = 'livings'


class RoomTypes(models.Model):
    rt_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0, verbose_name='ID')
    rtn = models.ForeignKey('RoomTypesNames', models.DO_NOTHING, verbose_name='Тип номера')
    rt_price = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Цена')
    rt_capacity = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Вместимость')
    rt_area = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Площадь')
    f = models.ForeignKey(Filials, models.DO_NOTHING, verbose_name='Филиал')

    def __str__(self):
        return self.rtn.rtn_name + "_" + self.f.f_name

    class Meta:
        verbose_name = 'тип номера в филиале'
        verbose_name_plural = 'типы номеров в филиалах'
        managed = False
        db_table = 'room_types'
        unique_together = (('rt_id', 'f'),)


class RoomTypesNames(models.Model):
    rtn_id = models.DecimalField(primary_key=True, max_digits=3, decimal_places=0, verbose_name='ID')
    rtn_name = models.CharField(unique=True, max_length=100, verbose_name='Тип номера')

    def __str__(self):
        return self.rtn_name

    class Meta:
        verbose_name = 'тип номера'
        verbose_name_plural = 'типы номеров'
        managed = False
        db_table = 'room_types_names'


class Rooms(models.Model):
    r_id = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0, verbose_name='ID')
    r_floor = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Этаж')
    rt = models.ForeignKey(RoomTypes, models.DO_NOTHING, verbose_name='Тип номера')
    f = models.ForeignKey(Filials, models.DO_NOTHING, verbose_name='Филиал')

    def __str__(self):
        return str(self.r_id) + "_" + self.f.f_name

    class Meta:
        verbose_name = 'номер'
        verbose_name_plural = 'номера'
        managed = False
        db_table = 'rooms'
        unique_together = (('r_id', 'rt'),)


class Statuses(models.Model):
    st_id = models.DecimalField(primary_key=True, max_digits=2, decimal_places=0, verbose_name='ID')
    st_name = models.CharField(unique=True, max_length=50, verbose_name='Статус')

    class Meta:
        verbose_name = 'статус бронирования'
        verbose_name_plural = 'статусы бронирования'
        managed = False
        db_table = 'statuses'

    def __str__(self):
        return self.st_name


class Work(models.Model):
    w_id = models.DecimalField(primary_key=True, max_digits=7, decimal_places=0, verbose_name='ID')
    e = models.ForeignKey(Employees, models.DO_NOTHING, verbose_name='Сотрудник')
    f = models.ForeignKey(Filials, models.DO_NOTHING, verbose_name='Филиал')
    j = models.ForeignKey(Jobs, models.DO_NOTHING, verbose_name='Должность')
    e_hired = models.DateField(verbose_name='Дата приёма')
    e_fired = models.DateField(blank=True, null=True, verbose_name='Дата увольнения')

    e.admin_order_field = 'e__e_name'

    def __str__(self):
        return "F" + str(self.f.f_id) + "_" + self.e.e_name + "_" + str(self.e.e_id)

    class Meta:
        verbose_name = 'работа в филиале'
        verbose_name_plural = 'работа в филиалах'
        managed = False
        db_table = 'work'
