from datetime import date, datetime, time, timezone
import calendar

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.db import connections, router
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from Hotels.models import Rooms

from .models import Bookings, Filials, Guests, Livings, Statuses
from .forms import GuestForm, FindEmptyRoomsForm


def main(request):
    return render(request, "index.html")


@login_required(login_url='/admin/login/')
def reports(request):
    rep = [
        ("Текущие сотрудники", "actual_emp"),
        ("Уволенные сотрудники", "fired_emp"),
        ("Свободные номера на сегодня", "empty_today"),
        ("Постоянные гости (по бронированиям)", "bookings5"),
        ("Постоянные гости (по проживаниям)", "livings5"),
        ("Долгосрочные проживания", "long_livings"),
        ("Статистика по регистрации гостей", "reg_stat"),
        ("Статистика по посещениям", "livings_stat"),
        ("Статистика по сотрудникам Reception", "arr_dep_stat"),
        ("Проживания гостей, которые выселились раньше", "early_dep"),
        ("Прибыль по филиалам", "profit"),
        ("Репликация", "replication"),
        ("Занятость номеров", "rooms_table")
    ]
    return render(request, 'reports.html', { "reports": rep })


@login_required(login_url="/admin/login")
def actual_emp(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
                select e.e_id AS "ID", e.e_name AS "ФИО", j.j_name AS "Должность", f.f_name AS "Филиал", w.e_hired AS "Дата приёма"
                from employees e
                join work w
                   on e.e_id=w.e_id
                join jobs j
                   on w.j_id=j.j_id
                join filials f
                   on w.f_id=f.f_id
                where current_date>=w.e_hired AND w.e_fired IS NULL
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html", {"data": data, "headers": headers, "name": "Текущие сотрудники"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def fired_emp(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
                select e.e_id AS "ID", e.e_name AS "ФИО", j.j_name AS "Должность", f.f_name AS "Филиал", w.e_hired AS "Дата приёма", w.e_fired AS "Дата увольнения"
                from employees e
	            join work w
	 	           on e.e_id=w.e_id
                join jobs j
                   on w.j_id=j.j_id
                join filials f
                   on w.f_id=f.f_id
                where w.e_fired IS NOT NULL
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html", {"data": data, "headers": headers, "name": "Уволенные сотрудники"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def empty_today(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
                select f.f_name AS "Филиал", rtn.rtn_name AS "Тип номера", r.r_id AS "Номер", rt.rt_price AS "Стоимость", rt.rt_capacity AS "Вместимость"
                from rooms r 
                    join room_types rt 
                        on r.rt_id=rt.rt_id
                    join room_types_names rtn
                        on rt.rtn_id=rtn.rtn_id
                    join filials f
                        on rt.f_id=f.f_id
                where NOT EXISTS(
                          select 1 from livings l 
                          where l.r_id=r.r_id 
                            AND current_date>=(l.l_arr_date::date) AND w_id_dep IS NULL
            );
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html", {"data": data, "headers": headers, "name": "Свободные номера на сегодня"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def bookings5(request):
    if request.user.groups.filter(name="replication").exists():
        if request.method == "GET":
            return render(request, "form.html", {"name": "Число бронирований", "name2": "бронирований",
                                                 "min": 1, "max": 10, "value": 5})
        else:
            num = request.POST.get('num')
            if not num:
                return HttpResponseServerError(
                    "<head><title>Ошибка</title></head><body><h1>Ошибка</h1><p>Введено некорректное значение, повторите попытку</p>"
                    "<p><a href=\"\">Вернуться</a></p></body>")
            else:
                connection = connections[router.db_for_read(Rooms)]
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    select b.g_id AS "ID гостя", g.g_name AS "ФИО", g.g_phone AS "Телефон", count(*) AS "Количество бронирований"
                    from bookings b 
                        join statuses st
                            on b.st_id=st.st_id
                        join guests g
                            on g.g_id=b.g_id
                    where lower(st.st_name) IN ('оплачено','забронировано')
                    group by b.g_id, g.g_name, g.g_phone
                    having count(*)>={num}
                        """)
                    data = [data for data in cursor]
                    headers = [header.name for header in cursor.description]
                return render(request, "report.html",
                              {"data": data, "headers": headers, "name": "Постоянные гости (по бронированиям)"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def livings5(request):
    if request.user.groups.filter(name="replication").exists():
        if request.method == "GET":
            return render(request, "form.html", {"name": "Число проживаний", "name2": "проживаний",
                                                 "min": 1, "max": 10, "value": 5})
        else:
            num = request.POST.get('num')
            if not num:
                return HttpResponseServerError(
                    "<head><title>Ошибка</title></head><body><h1>Ошибка</h1><p>Введено некорректное значение, повторите попытку</p>"
                    "<p><a href=\"\">Вернуться</a></p></body>")
            else:
                connection = connections[router.db_for_read(Rooms)]
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    select g.g_id AS "ID гостя", g.g_name AS "ФИО", g.g_phone AS "Телефон", count(*) AS "Количество проживаний"
                    from guests g 
                    join livings l
                    on g.g_id=l.g_id
                    where l.w_id_arr IS NOT NULL
                    group by g.g_id, g.g_name, g.g_phone
                    having count(*)>={num}
                        """)
                    data = [data for data in cursor]
                    headers = [header.name for header in cursor.description]
                return render(request, "report.html",
                              {"data": data, "headers": headers, "name": "Постоянные гости (по проживаниям)"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def long_livings(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
            select l.l_id AS "ID проживания", r.r_id AS "ID номера", rtn.rtn_name AS "Тип номера", f.f_name AS "Филиал", g.g_id AS "ID гостя", g.g_name AS "ФИО"
from guests g
	join livings l 
		on g.g_id=l.g_id
		join rooms r
		on r.r_id = l.r_id
           join room_types rt
			on l.rt_id=rt.rt_id
join room_types_names rtn
			on rt.rtn_id=rtn.rtn_id
	join filials f
			on f.f_id=rt.f_id

where l.w_id_arr IS NOT NULL
	AND CASE WHEN l.w_id_dep IS NOT NULL 
	then DATE_PART('day', l.l_dep_date - l.l_arr_date) >= 30
	ELSE DATE_PART('day', current_date - l.l_arr_date)>= 30 END
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html", {"data": data, "headers": headers, "name": "Долгосрочные проживания"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def reg_stat(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
            (select e.e_id AS "ID сотрудника", e.e_name AS "ФИО", f.f_name AS "Филиал", count(*) AS "Количество гостей"
            from guests g
                join work w
                    on g.w_id=w.w_id
                join employees e
                    on w.e_id=e.e_id
                join filials f
                    on f.f_id=w.f_id
            group by g.w_id, e.e_id, e.e_name, f.f_name
            UNION 
            select e.e_id AS "ID сотрудника", e.e_name AS "ФИО", f.f_name AS "Филиал", 0 AS "Количество гостей"
            from work w
                join employees e
                    on w.e_id=e.e_id
                join filials f
                    on f.f_id=w.f_id
            where NOT EXISTS(select 1 from guests g where g.w_id=w.w_id))
            ORDER BY "Филиал", "Количество гостей" DESC
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html",
                      {"data": data, "headers": headers, "name": "Статистика по регистрации гостей"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def livings_stat(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
                select f.f_name AS "Филиал", count(distinct g.g_id) AS "Количество проживаний"
                from guests g
                    join livings l
                        on l.g_id=g.g_id
                    join room_types rt
                        on l.rt_id=rt.rt_id
                    join filials f
                        on f.f_id=rt.f_id
                where DATE_PART('day', current_date - l.l_arr_date)<=30
                group by f.f_id, f.f_name
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html",
                      {"data": data, "headers": headers, "name": "Статистика по проживаниям за месяц"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def early_dep(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
            select l.l_id AS "ID проживания", l.b_id AS "ID бронирования", g.g_id AS "ID гостя", g.g_name AS "Гость", rtn.rtn_name AS "Тип номера", l.r_id as "Номер", l.l_arr_date AS "Дата заезда", l.l_dep_date AS "Дата выезда (факт)", b.b_dep_date AS "Дата выезда (план)"
            from bookings b
                join livings l
                    on b.b_id=l.b_id
                join guests g
                    on g.g_id=l.g_id
                join room_types rt
                    on rt.rt_id=l.rt_id
                join room_types_names rtn
                    on rtn.rtn_id=rt.rtn_id
            where b.b_dep_date!=(l.l_dep_date::date)
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html",
                      {"data": data, "headers": headers, "name": "Проживания гостей, которые выселились раньше"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def arr_dep_stat(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
            select COALESCE(arr.e_id, dep.e_id) as "ID сотрудника", COALESCE(arr.w_id, dep.w_id) as "ID работы в филиале", COALESCE(arr.e_name, dep.e_name) as "ФИО",
	   COALESCE(arr.f_name, dep.f_name) as "Филиал", COALESCE(arr.cnt,0) as "Количество заселений", COALESCE(dep.cnt,0) as "Количество выселений"
from (select l.w_id_arr as w_id, e.e_id as e_id, e.e_name as e_name,  w.f_id as f_id, f.f_name as f_name, count (*) as cnt
		from livings l join work w on l.w_id_arr=w.w_id
			join employees e on e.e_id=w.e_id
            join filials f on f.f_id = w.f_id
		where l.w_id_arr IS NOT NULL AND w.e_fired IS NULL
	  		AND DATE_PART('day', current_date - l.l_arr_date)<=30
		group by l.w_id_arr, e.e_id, e.e_name, w.e_id, w.f_id, f.f_name
	 ) as arr FULL JOIN 
	(select l.w_id_dep as w_id, e.e_id as e_id, e.e_name as e_name, w.f_id as f_id, f.f_name as f_name, count (*) as cnt
		from livings l join work w on l.w_id_dep=w.w_id
		join employees e on e.e_id=w.e_id
                                   join filials f on f.f_id = w.f_id
		where l.w_id_dep IS NOT NULL AND w.e_fired IS NULL
	 		AND DATE_PART('day', current_date - l.l_dep_date)<=30
		group by l.w_id_dep, e.e_id, e.e_name, w.e_id, w.f_id, f.f_name
	) as dep ON arr.w_id=dep.w_id
--работяги	
UNION
--халявщики
select e.e_id, w.w_id, e.e_name, f.f_name, 0, 0
from work w
	join employees e
		on w.e_id=e.e_id
	join filials f on f.f_id = w.f_id
where w.e_fired IS NULL
	AND NOT EXISTS(select 1 from livings l
				   where (l.w_id_arr=w.w_id AND DATE_PART('day', current_date - l.l_arr_date)<=30)
				   		OR (l.w_id_dep=w.w_id AND DATE_PART('day', current_date - l.l_dep_date)<=30)
				  )
order by 5 desc, 6 desc, 4 desc
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html",
                      {"data": data, "headers": headers, "name": "Статистика по сотрудникам Reception"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def profit(request):
    if request.user.groups.filter(name="replication").exists():
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("""
            select f.f_name as "Филиал", rtn.rtn_name as "Тип номера", l.r_id as "Номер", rt.rt_price AS "Стоимость", SUM(CASE WHEN l.l_dep_date IS NULL 
	   									THEN DATE_PART('day', current_date - l.l_arr_date)*rt.rt_price
									    ELSE DATE_PART('day', l.l_dep_date - l.l_arr_date)*rt.rt_price END) as "Прибыль"	
from rooms r
  	join livings l
    	on l.r_id=r.r_id AND l.w_id_arr IS NOT NULL --реально физически заселили
    join room_types rt 
        on l.rt_id=rt.rt_id
    join room_types_names rtn
        on rt.rtn_id=rtn.rtn_id
	join filials f
		on f.f_id=rt.f_id
where (CASE WHEN l.l_dep_date IS NULL 
	   	then DATE_PART('day', current_date - l.l_arr_date)<=30
	   ELSE DATE_PART('day', l.l_dep_date - l.l_arr_date)<=30 END)
group by f.f_name, rtn.rtn_name, l.r_id, rt.rt_price
                """)
            data = [data for data in cursor]
            headers = [header.name for header in cursor.description]
        return render(request, "report.html", {"data": data, "headers": headers, "name": "Прибыль по филиалам"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


@login_required(login_url="/admin/login")
def rooms_table(request):
    if request.user.groups.filter(name="replication").exists():
        now = datetime.now()
        if request.GET.get("year"):
            year = int(request.GET.get("year"))
        else:
            year = now.year
        if request.GET.get("month"):
            month = int(request.GET.get("month"))
        else:
            month = now.month
        if request.GET.get("month_year"):
            month_year = str(request.GET.get("month_year"))
            year = int(month_year[0:4])
            month = int(month_year[5:7])
        num_days = calendar.monthrange(year, month)[1]
        days = [date(year, month, day) for day in range(1, num_days + 1)]
        days.insert(0, "Номер")
        rooms = Rooms.objects.all()
        data = []
        for room in rooms:
            data.append([room, []])
            for day in days[1:]:
                connection = connections[router.db_for_read(Rooms)]
                with connection.cursor() as cursor:
                    cursor.execute(f"select free_today({room.r_id}, '{day}')")
                    res = [row for row in cursor][0][0]
                    if res:
                        data[-1][1].append('free')
                    else:
                        data[-1][1].append('busy')
        translate = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
                     9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
        return render(request, "rooms_table.html", {"data": data, "headers": days, "name": "Занятость номеров",
                                                    "month": f"{translate[month]} {year}", "year_value": f"{year:04}",
                                                    "month_value": f"{month:02}"})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


class ReplicationSlot:
    def __init__(self, data):
        self.data = list(data)
        cheffs = {
            "sub_system": "Маршутина Е.Н.",
            "sub_system_k": "Падалица К.А.",
            "sub_system_a": "Степченко А.С."
        }
        self.data.insert(1, None if data[0] not in cheffs else cheffs[data[0]])
        self.active = "active" if data[6] else "not_active"


@login_required(login_url='/admin/login/')
def replication(request):
    if request.user.groups.filter(name="replication").exists():
        translate = {
            "slot_name": "Слот репликации",
            "plugin": "Плагин",
            "slot_type": "Тип слота",
            "datoid": "OID БД",
            "database": "Имя БД",
            "temporary": "Временный",
            "active": "Активен",
            "active_pid": "ID процесса",
            "xmin": "ID транзакции для передачи",
            "catalog_xmin": "ID транзакции для передачи из системных каталогов",
            "restart_lsn": "Адрес записи в WAL",
            "confirmed_flush_lsn": "Адрес последней переданной транзакции",
            "wal_status": "Состояние файлов WAL",
            "safe_wal_size": "Объём хранения WAL",
            "two_phase": "Алгоритм двухфазной фиксации",
            "conflicting": "Конфликт"
        }
        connection = connections[router.db_for_read(Rooms)]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_replication_slots")
            data = [ReplicationSlot(data) for data in cursor]
            headers = [translate[header.name] for header in cursor.description]
        headers.insert(1, "Ответственный")
        return render(request, "replication.html", {"data": data, "headers": headers})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    context = { 'form': form }
    return render(request, 'login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['g_mail']
            guest = Guests(username=user.username)
            guest.g_id = Guests.objects.order_by('-g_id')[0].g_id + 1 if Guests.objects.order_by('-g_id') else 0;
            guest.g_name = form.cleaned_data['g_name']
            guest.g_gender = form.cleaned_data['g_gender']
            guest.g_born = form.cleaned_data['g_born']
            guest.g_phone = form.cleaned_data['g_phone']
            guest.g_mail = form.cleaned_data['g_mail']
            guest.g_passp = form.cleaned_data['g_passp']
            user.save()
            guest.save()
            login(request, user)
            return redirect('/')
    else:
        form = GuestForm()

    context = { 'form': form }
    return render(request, 'register.html', context)


@login_required(login_url='/admin/login/')
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def bookings(request):
    bookings_list = Bookings.objects.filter(g__username=request.user.username).order_by('-b_id')

    context = {
        'bookings_list': bookings_list,
    }
    return render(request, 'bookings.html', context)


@login_required(login_url='/login/')
def find_empty_rooms(request):
    if request.method == 'POST':
        form = FindEmptyRoomsForm(request.POST)
        if form.is_valid():
            filial_id = int(form.cleaned_data['filial'])
            print(filial_id)
            arrival_date = form.cleaned_data['arrival_date']
            departure_date = form.cleaned_data['departure_date']
            with connections["hotels"].cursor() as cursor:
                cursor.execute('SELECT r_id AS "Номер", rtn_name AS "Тип номера", rt_price AS "Стоимость", rt_capacity AS "Вместимость" FROM free_rooms(%s, %s, %s)', [filial_id, arrival_date, departure_date])
                rows = cursor.fetchall()
                headers = [header.name for header in cursor.description]

            context = {
                'filial': Filials.objects.get(pk=filial_id),
                'arrival_date': arrival_date,
                'departure_date': departure_date,
                'rows': rows,
                'headers': headers,
            }
            return render(request, 'available_rooms.html', context)
    else:
        form = FindEmptyRoomsForm()

    context = { 'form': form }
    return render(request, 'find_empty_rooms.html', context)


@login_required(login_url='/admin/login/')
def book_room(request, room_id: int, arr_year: int, arr_month: int, arr_day: int, dep_year: int, dep_month: int, dep_day: int):
    room = Rooms.objects.get(pk=room_id)
    filial = room.f
    arrival_date = date(arr_year, arr_month, arr_day)
    departure_date = date(dep_year, dep_month, dep_day)

    if request.method == 'POST':
        with connections["hotels"].cursor() as cursor:
            cursor.execute('SELECT r_id AS "Номер", rtn_name AS "Тип номера", rt_price AS "Стоимость", rt_capacity AS "Вместимость" FROM free_rooms(%s, %s, %s) WHERE r_id = %s', [filial.f_id, arrival_date, departure_date, room_id])
            if not cursor.fetchall():
                return HttpResponseBadRequest("Уже забронированно")

        booking = Bookings()
        booking.b_id = Bookings.objects.order_by('-b_id')[0].b_id + 1
        booking.b_book_date = datetime.now()
        booking.rt = room.rt
        booking.g = Guests.objects.filter(username=request.user.username)[0]
        booking.b_arr_date = arrival_date
        booking.b_dep_date = departure_date
        booking.st = Statuses.objects.filter(st_name='Забронировано')[0]
        living = Livings()
        living.l_id = Livings.objects.order_by('-l_id')[0].l_id + 1
        living.b = booking
        living.rt = booking.rt
        living.r = room
        living.g = booking.g
        living.l_arr_date = datetime.combine(arrival_date, time(0, 0), timezone.utc)
        living.l_dep_date = datetime.combine(departure_date, time(0, 0), timezone.utc)
        booking.save()
        living.save()
        return redirect('/')

    context = {
        'room': room,
        'filial': filial,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
    }
    return render(request, 'book_room.html', context)
