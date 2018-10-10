from datetime import timedelta, date
from functools import reduce


# 一ヶ月分のカレンダーを作成するクラス
class CalResolver:

    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.date = date(year, month, int(1))
        self.shift = (lambda x: x - timedelta(days=x.weekday() + 1))
        self.addWeek = (lambda date, week: date + timedelta(weeks=week))
        self.week = self.__alldaysOfWeek__()
        self.weeks = len(self.week)

    def __alldaysOfWeek__(self):
        shiftDate = self.shift(self.date)
        result = [
            self.__daysOfWeek__(shiftDate - timedelta(weeks=1)),
            self.__daysOfWeek__(shiftDate),
        ]
        if self.__isNextOrPrevMonth__(result[0], result[1]):
            del(result[0])
        for i in range(1, 10):
            after = self.addWeek(shiftDate, i)
            if after.month != self.month:
                break
            result.append(self.__daysOfWeek__(after))
        result.append(
            self.__daysOfWeek__(
                self.addWeek(
                    shiftDate,
                    len(result)
                )
            )
        )

        if self.__isNextOrPrevMonth__(result[len(result) - 1]):
            del(result[len(result) - 1])
        return result

    def __daysOfWeek__(self, target):
        result = {}
        result[1] = {
                "dayOfWeek": self.getDayOfWeek(target.weekday() + 1),
                "date": target,
        }
        for i in range(1, 7):
            obj = target + timedelta(days=i)
            result[i + 1] = {
                "dayOfWeek": self.getDayOfWeek(obj.weekday() + 1),
                "date": obj,
            }
        return result

    def __isNextOrPrevMonth__(self, *weeks):
        # match = (lambda x, m: x == m)
        notmatch = (lambda x, m: x != m)
        # for文グルグル 集約
        walk = (lambda x, c, f: reduce(
            c,
            [f(x[e]["date"].month, self.month) for e in x])
        )
        # for in the for super
        walkinwalk = (lambda x, c, f: [walk(e, c, f) for e in x])
        results = []
        if len(weeks) == 0:
            return False
        elif len(weeks) == 1:
            results.append(walk(weeks[0], comp, notmatch))
        else:
            results.append(walk(weeks[0], comp, notmatch))
            # 厳密な検査
            results.extend(walkinwalk(weeks[1:], strictComp, notmatch))
        return allTrue(results)

    def nextOrPrevWeek(self, week: int):
        nop = self.nextOrPrev(week)
        if nop["prev"] is None and nop["next"] is None:
            return nop
        else:
            return {
                "prev": {
                    "year": nop["prev"]["year"],
                    "month": nop["prev"]["month"],
                    "week": nop["prev"]["weekNum"],
                },
                "next": {
                    "year": nop["next"]["year"],
                    "month": nop["next"]["month"],
                    "week": nop["next"]["weekNum"],
                }
            }
    '''
    指定された週番号から一週間前と一週間後の情報が示された
    ディクショナリを返す
    '''
    def nextOrPrev(self, week: int):
        result = {"prev": None, "next": None}
        # return as Empty Dictionary
        if week < 0 or self.weeks <= week:
            return result

        if week == 0:
            year = self.year
            month = self.month
            prev_cal = None
            p_mon = 0
            p_year = 0
            if month == 1:
                p_mon = 12
                p_year = year - 1
            else:
                p_mon = month - 1
                p_year = year
            prev_cal = CalResolver(p_year, p_mon)
            result["prev"] = {
                "year": p_year,
                "month": p_mon,
                "week": prev_cal.week[prev_cal.weeks-1],
                "weekNum": prev_cal.weeks-1
            }
            result["next"] = {
                "year": year,
                "month": month,
                "week": self.week[week+1],
                "weekNum": week+1
            }
        # To specify last week number
        elif week == self.weeks - 1:
            year = self.year
            month = self.month
            next_cal = None
            n_mon = 0
            n_year = 0
            if month == 12:
                n_mon = 1
                n_year = year + 1
            else:
                n_mon = month + 1
                n_year = year
            next_cal = CalResolver(n_year, n_mon)
            next_weeknum = 2
            # specifyed week dict is when this week
            if not self.__isNextOrPrevMonth__(self.week[week]):
                next_weeknum = 1
            result["prev"] = {
                "year": year,
                "month": month,
                "week": self.week[week - 1],
                "weekNum": week-1
            }
            result["next"] = {
                "year": n_year,
                "month": n_mon,
                "week": next_cal.week[2],
                "weekNum": next_weeknum
            }
        else:
            year = self.year
            month = self.month
            result["prev"] = {
                "year": year,
                "month": month,
                "week": self.week[week-1],
                "weekNum": week-1
            }
            result["next"] = {
                "year": year,
                "month": month,
                "week": self.week[week+1],
                "weekNum": week+1
            }
        return result

    # 指定した日付から、月の初めから何周目かを計算する
    def getWeek(self, date):
        weeks = self.week
        count = 0
        result = 0
        flag = False
        for week in weeks:
            for day in week:
                if week[day]["date"] == date:
                    flag = True
            if flag:
                result = count
                break
            count += 1
        return result

    def getDayOfWeek(self, dow: int):
        WEEK_DICT = {
            1: "月",
            2: "火",
            3: "水",
            4: "木",
            5: "金",
            6: "土",
            7: "日"
        }
        if 1 <= dow <= 7:
            return WEEK_DICT[dow]
        else:
            return ""


def allTrue(list):
    for e in list:
        if e is not True:
            return False
    return True


def comp(x, y):
    And = (lambda x, y: x is True and y is True)
    Or = (lambda x, y: x is True and y is False)
    if And(x, y):
        return x
    elif Or(x, y):
        return True
    elif Or(y, x):
        return True
    else:
        return False


def strictComp(x, y):
    And = (lambda x, y: x is True and y is True)
    return And(x, y)
