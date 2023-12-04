from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.db import connection
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
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
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pg_replication_slots")
            data = [ReplicationSlot(data) for data in cursor]
            headers = [translate[header.name] for header in cursor.description]
        headers.insert(1, "Ответственный")
        return render(request, "replication.html", {"data": data, "headers": headers})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1><a href="/admin/logout">Выход</a>')