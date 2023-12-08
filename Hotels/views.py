from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.db import connections
from django.contrib.auth.decorators import login_required
import datetime, calendar
from Hotels.models import Rooms


# Create your views here.

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
    html = '<p><a href="/">Назад</a></p><br>'
    for report in rep:
        html += f'<p><a href="{report[1]}">{report[0]}</a></p>'
    return HttpResponse(f"<h1>Отчётные формы</h1>{html}")


@login_required(login_url="/admin/login")
def actual_emp(request):
    if request.user.groups.filter(name="replication").exists():
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
                with connections["hotels"].cursor() as cursor:
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
                with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        with connections["hotels"].cursor() as cursor:
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
        now = datetime.datetime.now()
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
        days = [datetime.date(year, month, day).strftime("%d.%m.%Y") for day in range(1, num_days + 1)]
        days.insert(0, "Номер")
        rooms = Rooms.objects.all()
        data = []
        for room in rooms:
            data.append([room, []])
            for day in days[1:]:
                with connections["hotels"].cursor() as cursor:
                    cursor.execute(f"select is_free_today({room.r_id}, '{day}')")
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
        with connections["hotels"].cursor() as cursor:
            cursor.execute("SELECT * FROM pg_replication_slots")
            data = [ReplicationSlot(data) for data in cursor]
            headers = [translate[header.name] for header in cursor.description]
        headers.insert(1, "Ответственный")
        return render(request, "replication.html", {"data": data, "headers": headers})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')
