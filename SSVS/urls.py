from django.urls import path

from . import views

app_name = 'SSVS'
urlpatterns = [
    path('', views.index, name="index"),
    path('schedule.json', views.scheduleJson, name="schedule.json"),
    path(
        "week/<int:year>/<int:month>/<int:week>",
        views.weekOfSchedule,
        name="weekOfSchedule"),
    path(
        "day/<int:year>/<int:month>/<int:day>",
        views.dayOfSchedule,
        name="dayOfSchedule"),
    # path("schedule/form", views.renderScheduleForm, name="scheduleForm"),
    path(
        "day/<int:year>/<int:month>/<int:day>/form",
        views.renderScheduleForm,
        name="scheduleForm"),
    path(
        "day/<int:year>/<int:month>/<int:day>/register",
        views.registerSchedule,
        name="scheduleRegitser"),
    # path(
    #     "schedule/register",
    #     views.registerSchedule,
    #     name="scheduleRegitser"),
]
