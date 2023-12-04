from django.contrib import admin
from django.forms import ModelForm
# Register your models here.

from .models import Bookings, Employees, Filials, Guests, Jobs, Livings, RoomTypes, RoomTypesNames, Rooms, Statuses, \
    Work

class BookingsInline(admin.TabularInline):
    model = Bookings
    extra = 1

class LivingsInline(admin.StackedInline):
    model = Livings
    extra = 1

class WorkInline(admin.TabularInline):
    model = Work
    extra = 1


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ("e_name", "e_gender", "e_born", "e_passp", "e_phone","e_addr")
    list_filter = ["e_gender"]
    search_fields = ["e_name", "e_passp", "e_phone", "e_addr"]

    inlines = [
        WorkInline
    ]
    ordering = ['e_name']
    list_per_page = 15

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["e_id"].disabled = True
        return form

@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "rt", "b_arr_date", "b_dep_date", "status")
    list_filter = ['rt', 'st']
    search_fields = []

    def guest_name(self, obj):
        return str(obj.g)

    def room_type(self, obj):
        return obj.rt.rtn.rtn_name + " | " + obj.rt.f.f_name

    def status(self, obj):
        return obj.st.st_name

    inlines = [
        LivingsInline
    ]

    guest_name.short_description = 'Гость'
    guest_name.admin_order_field = 'g__g_name'
    room_type.short_description = 'Тип номера'
    room_type.admin_order_field = 'rt'
    status.short_description = 'Статус'
    status.admin_order_field = 'st__st_name'
    ordering = ['g__g_name', '-b_arr_date']
    list_per_page = 30

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["b_id"].disabled = True
        return form

@admin.register(Filials)
class FilialsAdmin(admin.ModelAdmin):
    list_display = ['f_name', 'f_addr', 'f_phone', 'f_mail', 'f_open']
    list_filter = ['f_open']

    ordering = ['f_name']
    list_per_page = 15

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["f_id"].disabled = True
        return form

@admin.register(Guests)
class GuestsAdmin(admin.ModelAdmin):
    list_display = ("g_name", "g_gender", "g_born", "g_passp", "g_phone")
    list_filter = ["g_gender"]

    inlines = [
        BookingsInline, LivingsInline
    ]
    ordering = ['g_name']
    list_per_page = 30

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["g_id"].disabled = True
        return form

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ['j_name', 'j_salary']

    ordering = ["j_name"]
    list_per_page = 30

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["j_id"].disabled = True
        return form

@admin.register(Livings)
class LivingsAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "booking", "rt", "l_arr_date", "l_dep_date")
    list_filter = ["rt"]

    def guest_name(self, obj):
        return obj.g.g_name

    def booking(self, obj):
        return obj.b if obj.b is not None else "без брони"

    guest_name.short_description = 'Гость'
    guest_name.admin_order_field = 'g__g_name'
    booking.short_description = 'Бронирование'
    booking.admin_order_field = 'b'

    ordering = ["-l_arr_date"]
    list_per_page = 30

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["l_id"].disabled = True
        return form


@admin.register(RoomTypesNames)
class RoomTypesNamesAdmin(admin.ModelAdmin):
    list_display = ['rtn_name']

    ordering = ['rtn_name']
    list_per_page = 15

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["rtn_id"].disabled = True
        return form

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ['r_id', 'room_type', 'r_floor', 'filial_name']
    list_filter = ['f', 'rt__rtn']

    def filial_name(self, obj):
        return obj.f.f_name

    def room_type(self, obj):
        return obj.rt.rtn.rtn_name

    filial_name.short_description = 'Филиал'
    filial_name.admin_order_field = 'f__f_name'
    room_type.short_description = 'Тип номера'
    room_type.admin_order_field = 'rt__rtn__rtn_name'

    ordering = ['f__f_name', 'r_id']
    list_per_page = 30

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["r_id"].disabled = True
        return form

@admin.register(Statuses)
class StatusesAdmin(admin.ModelAdmin):
    list_display = ('st_name', )

    ordering = ["st_name"]
    list_per_page = 15

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["st_id"].disabled = True
        return form

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("emp_name", "filial_name", "job_name", "e_hired", "e_fired")
    list_filter = ("f", )

    def emp_name(self, obj):
        return str(obj.e)

    def filial_name(self, obj):
        return obj.f.f_name

    def job_name(self, obj):
        return obj.j.j_name

    list_per_page = 30
    ordering = ['f__f_name', 'e__e_name']
    emp_name.short_description = 'Сотрудник'
    emp_name.admin_order_field = 'e__e_name'
    filial_name.short_description = 'Филиал'
    filial_name.admin_order_field = 'f__f_name'
    job_name.short_description = 'Должность'
    job_name.admin_order_field = 'j__j_name'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["w_id"].disabled = True
        return form

@admin.register(RoomTypes)
class RoomTypesAdmin(admin.ModelAdmin):
    list_display = ("room_type_name", "filial_name", "rt_price", "rt_capacity")
    list_filter = ["f", "rtn"]

    def room_type_name(self, obj):
        return obj.rtn.rtn_name

    def filial_name(self, obj):
        return obj.f.f_name


    ordering = ["f__f_name", "rtn__rtn_name"]
    list_per_page = 15

    room_type_name.short_description = 'Тип номера'
    room_type_name.admin_order_field = 'rtn__rtn_name'
    filial_name.short_description = 'Филиал'
    filial_name.admin_order_field = 'f__f_name'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["rt_id"].disabled = True
        return form