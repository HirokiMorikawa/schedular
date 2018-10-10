from django.contrib import admin
from SSVS.models import (
        Teacher,
        Student,
        Subject,
        ChargeSubject,
        School,
        Lesson,
        TimeInterval,
        Schedule)


# adminページの見た目の設定
# admin.site.register(Teacher)
# admin.site.register(Subject)
# admin.site.register(ChargeSubject)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',)
    list_display_links = ('first_name', 'last_name',)


# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'subject_list',)
#     list_display_links = ('subject_list',)
#
#
# class ChargeSubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'teacher', 'subject', )
#     list_display_links = ('teacher', )


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'school_name')
    list_display_links = ('school_name', )


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'time',
        'school', 'teacher',
        'lesson', 'student',
        'update_at', )
    list_display_links = ('date', )


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
# admin.site.register(Subject, SubjectAdmin)
# admin.site.register(ChargeSubject, ChargeSubjectAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Lesson)
admin.site.register(TimeInterval)
admin.site.register(Schedule, ScheduleAdmin)
