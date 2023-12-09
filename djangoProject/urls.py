"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Hotels import views

urlpatterns = [
    path('', views.main),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('bookings/', views.bookings),
    path('find_empty_rooms/', views.find_empty_rooms),
    path('book_room/<int:room_id>/<int:arr_year>/<int:arr_month>/<int:arr_day>/<int:dep_year>/<int:dep_month>/<int:dep_day>/', views.book_room),
    path('reports/', views.reports),
    path('reports/actual_emp/', views.actual_emp),
    path('reports/fired_emp/', views.fired_emp),
    path('reports/empty_today/', views.empty_today),
    path('reports/replication/', views.replication),
    path('reports/bookings5/', views.bookings5),
    path('reports/livings5/', views.livings5),
    path('reports/reg_stat/', views.reg_stat),
    path('reports/livings_stat/', views.livings_stat),
    path('reports/long_livings/', views.long_livings),
    path('reports/early_dep/', views.early_dep),
    path('reports/profit/', views.profit),
    path('reports/arr_dep_stat/', views.arr_dep_stat),
    path('reports/rooms_table/', views.rooms_table),
    path('admin/', admin.site.urls)
]
