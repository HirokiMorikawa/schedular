import pytz
from datetime import date, datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.http import JsonResponse

from .models import Teacher, Schedule, Lesson
from .forms import ScheduleFormSet, ScheduleModelFormSet
from .calendarLib import CalResolver


def index(request):
    return render(request, "SSVS/cal.html", context=None)


# scheduleデータを取得する処理
def scheduleJson(request):
    scheduleList = []

    # intervals = []

    # testCode ScheduleクラスのField timeを取り出してリストにする
    for schedule in Schedule.objects.all():
        time = schedule.time
        lesson = schedule.lesson
        teacher = schedule.teacher
        school = schedule.school
        student = schedule.student.getStudentName()
        date = schedule.date
        start_time = time.start_time
        end_time = time.end_time

        start = datetime.combine(date, start_time)
        end = datetime.combine(date, end_time)

        start = pytz.timezone(settings.TIME_ZONE).localize(start)
        end = pytz.timezone(settings.TIME_ZONE).localize(end)

        title = lesson.lessonName + "["+teacher.name + "] "
        scheduleList_dict = {
            "id": schedule.id,
            "title": title,
            "content":  student,
            "school": school.school_name,
            "start": isoformatStr(start),
            "end": isoformatStr(end),
            "date": isoformatStr(date),
        }
        scheduleList.append(scheduleList_dict)
    # responseData = serializers.serialize("json", intervals)
    return JsonResponse(scheduleList, safe=False)


def teacherList(request):
    teacher_list = Teacher.objects.all()
    context = {"teacher_list": teacher_list}
    return render(request, "SSVS/teacher_list.html", context)


# 1週間分のスケジュールの表示
def weekOfSchedule(request, year, month, week):
    if month < 1 or 12 < month:
        return HttpResponse(status=404)
    cal: CalResolver = CalResolver(year, month)
    if week < 0 or cal.weeks <= week:
        return HttpResponse(status=404)
    now = datetime.now()
    thisMonth = now.month
    thisYear = now.year
    ndate = now.date()
    thisWeek = CalResolver(thisYear, thisMonth).getWeek(ndate)
    weekdayList = []
    nop = cal.nextOrPrevWeek(week)
    for day in cal.week[week]:
        # schedule_list = []

        cal_date = cal.week[week][day]
        # 日付ごとのスケジュールデータ
        schedules = Schedule.objects.filter(date=cal_date["date"])
        schedules = schedules.order_by("time", "lesson")

        weekdayList.append({
            "year": cal_date["date"].year,
            "month": cal_date["date"].month,
            "day": cal_date["date"].day,
            "dayOfWeek": cal_date["dayOfWeek"],
            "id": dTimeDate(cal_date["date"]),
            "week_count": day - 1,
            "schedules": schedules,
            "numOfSchedule": schedules.count()
        })
    context = {
        "year": year,
        "month": month,
        # 1週間後
        "next": reverse(
                "SSVS:weekOfSchedule",
                kwargs={
                    "year": nop["next"]["year"],
                    "month": nop["next"]["month"],
                    "week": nop["next"]["week"],
                }
        ),
        # 1週間前
        "prev": reverse(
                "SSVS:weekOfSchedule",
                kwargs={
                    "year": nop["prev"]["year"],
                    "month": nop["prev"]["month"],
                    "week": nop["prev"]["week"],
                }
        ),
        # 現在
        "now": reverse(
                "SSVS:weekOfSchedule",
                kwargs={
                    "year": thisYear,
                    "month": thisMonth,
                    "week": thisWeek,
                }
        ),
        "week_count": week,
        "week_list": weekdayList,
    }
    return render(request, "SSVS/w_schedule.html", context)


# 1日分のスケジュールの表示
def dayOfSchedule(request, year, month, day):
    # パラメータからdatetimeオブジェクトの生成
    s_date = datetime(year, month, day)

    next = s_date + timedelta(days=1)
    prev = s_date - timedelta(days=1)

    # Scheduleスキーマのクエリー発行
    schedule_list = (
        Schedule.objects.filter(date=s_date))
    # schedule_list = sorted(schedule_list,  key=lambda x: x.time.start_time)
    # 抽出データ格納用
    dist_list = []
    value = 1
    # Lessonスキーマからデータを一つずつ取得
    for lesson in Lesson.objects.all():
        # Lessonでschedule_listを抽出
        result = schedule_list.filter(lesson=lesson)
        if 0 is not len(result):
            # ソート
            result = sorted(result, key=lambda x: x.time.start_time)
            dist_list.append(
                {
                    "value": "value" + str(value),
                    "lesson": lesson,
                    "schedule_list": result,
                })
            value += 1
    context = {
        "date": dTimeDate(s_date),
        "next": reverse(
            "SSVS:dayOfSchedule",
            kwargs={
                "year": next.year,
                "month": next.month,
                "day": next.day
            }),
        "prev": reverse(
            "SSVS:dayOfSchedule",
            kwargs={
                "year": prev.year,
                "month": prev.month,
                "day": prev.day
            }),
        "year": year,
        "month": month,
        "day": day,
        "group": dist_list,
    }
    return render(request, "SSVS/d_schedule2.html", context)


# スケジュール登録フォームのviewをレンダリングする
def renderScheduleForm(request, year, day, month):
    # 検証後データの存在チェック
    if "form_data" in request.session:
        # 検証結果からフォームを作成する
        formset = ScheduleFormSet(request.session["form_data"])
        del request.session["form_data"]
    else:

        formset = ScheduleFormSet()

    # templateに渡す変数の定義
    context = {
        "formset": formset,
        "date": f'{year}年{month}月{day}日',
        "action_path": reverse(
            "SSVS:scheduleRegitser",
            kwargs={
                "year": year,
                "month": month,
                "day": day
            }),
        "method_type": "POST",
    }
    # viewのレンダリング
    return render(request, "SSVS/schedule_form.html", context)


# スケジュール登録フォームからPOSTリクエストにより
# データを受信してデータベースに登録する
@require_POST
def registerSchedule(request, year, month, day):
    date = datetime(year, month, day)
    formSet = ScheduleModelFormSet(
        request.POST
    )
    request.session['form_data'] = None

    # 入力データの検証
    if formSet.is_valid():
        forms = formSet.save(commit=False)
        for form in forms:

            form.date = date
            form.save()
        # リダイレクト
        return HttpResponseRedirect(reverse("SSVS:index"))
    else:
        # セッションにrequestデータを取り込む
        request.session['form_data'] = request.POST
        # リダイレクト
        return HttpResponseRedirect(
            reverse(
                "SSVS:scheduleForm",
                kwargs={
                    "year": year,
                    "month": month,
                    "day": day
                }))


# iso8601に基づいてdatetimeを文字列に変換する
def isoformatStr(d):
    return d.isoformat()


def dTimeDate(d):
    return d.strftime("%Y-%m-%d")


# 日付時間を文字列に変換する
def dTime(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")


def getDayOfWeek(dow: int):
    WEEK_DICT = {
        "0": "月",
        "1": "火",
        "2": "水",
        "3": "木",
        "4": "金",
        "5": "土",
        "6": "日"
    }
    if 0 <= dow <= 6:
        return WEEK_DICT[str(dow)]
    else:
        return ""
