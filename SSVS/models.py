import datetime
from django.utils import timezone
from django.db import models


# 講師データ
class Teacher(models.Model):
    name = models.CharField('氏名', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "講師データ"
        verbose_name_plural = "講師リスト"


# 生徒データ
class Student(models.Model):
    first_name = models.CharField('姓', max_length=255)
    last_name = models.CharField('名', max_length=255)

    def getStudentName(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "生徒データ"
        verbose_name_plural = "生徒リスト"


# 教科
class Subject(models.Model):
    SUBJECT_LIST = (
        ('その他', 'その他'),
        ('演習', '演習'),
        ('専門', '専門'),
        ('テスト対策', 'テスト対策'),
        ('テスト対策（中間）', 'テスト対策（中間）'),
        ('テスト対策（期末）', 'テスト対策(期末)'),
        ('受験対策', '受験対策'),
        ('受験対策（小学生）', '受験対策（小学生）'),
        ('受験対策（中学生）', '受験対策（中学生）'),
        ('受験対策（高校生）', '受験対策（高校生）'),
        ('国語', '国語'),
        ('現代文', '現代文'),
        ('古文', '古文'),
        ('漢文', '漢文'),
        ('数学', '数学'),
        ('数学A', '数学A'),
        ('数学B', '数学B'),
        ('数学I', '数学I'),
        ('数学II', '数学II'),
        ('数学III', '数学III'),
        ('数学演習', '数学演習'),
        ('英語', '英語'),
        ('リーディング', 'リーディング'),
        ('ライティング', 'ライティング'),
        ('理科', '理科'),
        ('物理', '物理'),
        ('物理基礎', '物理基礎'),
        ('生物', '生物'),
        ('生物基礎', '生物基礎'),
        ('化学', '化学'),
        ('化学基礎', '化学基礎'),
        ('社会', '社会'),
        ('歴史', '歴史'),
        ('日本史', '日本史'),
        ('世界史', '世界史'),
        ('現代史', '現代史'),
        ('公民', '公民'),
        ('地理', '地理'),
        ('P', 'Progmaming'),
        ('Web開発入門', 'Web開発入門'),
        ('プログラム開発手法', 'プログラム開発手法')
    )

    subject_list = models.CharField('科目', max_length=200, choices=SUBJECT_LIST)

    def __str__(self):
        return self.subject_list

    class Meta:
        verbose_name = "科目"
        verbose_name_plural = "科目リスト"


# 担当教科
class ChargeSubject(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='担当講師',
        on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject,
        verbose_name='科目',
        on_delete=models.PROTECT)

    def __str__(self):
        return self.teacher.name + "(" + self.subject.subject_list + ")"

    class Meta:
        verbose_name = "担当教科"
        verbose_name_plural = "講師の担当教科リスト"


# 校舎
class School(models.Model):
    school_name = models.CharField('校舎名', max_length=255)

    def __str__(self):
        return self.school_name

    class Meta:
        verbose_name = "校舎名"
        verbose_name_plural = "校舎リスト"


class Lesson(models.Model):
    lessonName = models.CharField("授業種類", max_length=50)

    def __str__(self):
        return self.lessonName

    class Meta:
        verbose_name = "授業名"
        verbose_name_plural = "授業リスト"


# 時刻
class TimeInterval(models.Model):
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))

    def getStart(self):
        return self.start_time

    def getEnd(self):
        return self.end_time

    def __str__(self):
        return (
            self.start_time.strftime("%H:%M") + "~" +
            self.end_time.strftime("%H:%M"))

    class Meta:
        verbose_name = "時刻"
        verbose_name_plural = "時刻リスト"


# スケジュール
class Schedule(models.Model):
    date = models.DateField('日付')
    time = models.ForeignKey(
        TimeInterval,
        verbose_name="時間",
        on_delete=models.PROTECT)
    school = models.ForeignKey(
        School,
        verbose_name="校舎",
        on_delete=models.PROTECT
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name="授業",
        on_delete=models.PROTECT
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name="講師",
        on_delete=models.PROTECT
    )
    student = models.ForeignKey(
        Student,
        verbose_name="生徒",
        on_delete=models.PROTECT
    )
    update_at = models.DateTimeField(
        '更新日',
        default=timezone.now,
        editable=False)

    def __str__(self):
        return (
            self.date.strftime("%Y/%m/%d") +
            self.lesson.lessonName +
            "[" +
            self.teacher.name +
            "]" +
            self.student.getStudentName() +
            "の授業")

    class Meta:
        verbose_name = "スケジュール詳細"
        verbose_name_plural = "スケジュール"
        unique_together = (
            "date", "time", "school", "lesson", "teacher", "student"
        )
